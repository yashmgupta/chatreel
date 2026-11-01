"""Single-instance, persistent, bounded render queue and authenticated Action API."""
import asyncio
from contextlib import asynccontextmanager
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import signal
import sqlite3
import sys
import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from render import validate, STYLES

DATA=Path(os.environ.get('JOB_DIR',str(ROOT/'.jobs'))).resolve()
API_KEY=os.environ.get('RENDER_API_KEY','')
BASE=os.environ.get('PUBLIC_BASE_URL','http://localhost:8000').rstrip('/')
TIMEOUT=int(os.environ.get('RENDER_TIMEOUT','300'))
TTL=int(os.environ.get('JOB_TTL','86400'))
MAX_BODY=65536
MAX_QUEUE=8
MAX_DISK=2*1024**3
JOB_BYTES=512*1024**2


def db():
    conn=sqlite3.connect(DATA/'queue.sqlite',timeout=5)
    conn.row_factory=sqlite3.Row
    return conn


def change(sql,args=()):
    with db() as c:c.execute(sql,args)


def expire():
    with db() as c:
        rows=c.execute("SELECT id FROM jobs WHERE status IN ('completed','failed') AND updated < ?",(time.time()-TTL,)).fetchall()
        for row in rows:
            shutil.rmtree(DATA/row['id'],ignore_errors=True)
            c.execute('DELETE FROM jobs WHERE id=?',(row['id'],))


def used_bytes():
    return sum(p.stat().st_size for p in DATA.rglob('*') if p.is_file())


def stop_process(proc):
    if proc.returncode is None:
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass


async def worker():
    while True:
        expire()
        with db() as c:
            c.execute('BEGIN IMMEDIATE')
            job=c.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY created LIMIT 1").fetchone()
            if job:c.execute("UPDATE jobs SET status='running',updated=? WHERE id=?",(time.time(),job['id']))
        if not job:
            await asyncio.sleep(.5);continue
        folder=DATA/job['id'];proc=None
        try:
            with (folder/'worker.log').open('wb') as log:
                proc=await asyncio.create_subprocess_exec(sys.executable,str(ROOT/'server/worker.py'),str(folder),
                    stdout=log,stderr=log,start_new_session=True)
                deadline=time.monotonic()+TIMEOUT
                while proc.returncode is None:
                    if time.monotonic()>deadline:raise TimeoutError('Render exceeded time limit')
                    if sum(p.stat().st_size for p in folder.rglob('*') if p.is_file())>JOB_BYTES:
                        raise RuntimeError('Render exceeded output size limit')
                    await asyncio.sleep(.2)
                if proc.returncode:raise RuntimeError('Render failed; check server worker.log (voice may exceed scene or Chromium sandbox may be unavailable)')
            result=json.loads((folder/'result.json').read_text())
            change("UPDATE jobs SET status='completed',result=?,updated=? WHERE id=?",(json.dumps(result),time.time(),job['id']))
        except asyncio.CancelledError:
            if proc:stop_process(proc);await proc.wait()
            change("UPDATE jobs SET status='failed',error='Server stopped during render',updated=? WHERE id=?",(time.time(),job['id']))
            raise
        except Exception as e:
            if proc:stop_process(proc);await proc.wait()
            (folder/'film.mp4').unlink(missing_ok=True)
            change("UPDATE jobs SET status='failed',error=?,updated=? WHERE id=?",(str(e),time.time(),job['id']))


@asynccontextmanager
async def lifespan(app):
    if len(API_KEY)<24:raise RuntimeError('Set RENDER_API_KEY to a random secret of at least 24 characters')
    DATA.mkdir(parents=True,exist_ok=True)
    lock=(DATA/'instance.lock').open('a')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise RuntimeError('Use one Uvicorn worker per JOB_DIR')
    with db() as c:
        c.execute('CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,status TEXT,created REAL,updated REAL,result TEXT,error TEXT)')
        c.execute("UPDATE jobs SET status='failed',error='Interrupted by server restart',updated=? WHERE status='running'",(time.time(),))
    task=asyncio.create_task(worker())
    try:yield
    finally:
        task.cancel()
        try:await task
        except asyncio.CancelledError:pass
        lock.close()


app=FastAPI(title='Chatreel render service',version='2.0.0',lifespan=lifespan)


def auth(request:Request):
    candidate=request.headers.get('X-API-Key','')
    if not API_KEY or not secrets.compare_digest(candidate.encode(),API_KEY.encode()):
        raise HTTPException(401,'Invalid API key')


def get_job_row(job_id):
    if not re.fullmatch('[0-9a-f]{32}',job_id):raise HTTPException(404,'Job not found')
    with db() as c:row=c.execute('SELECT * FROM jobs WHERE id=?',(job_id,)).fetchone()
    if not row:raise HTTPException(404,'Job not found or expired')
    return row


def signature(job_id,expires):
    return hmac.new(API_KEY.encode(),f'{job_id}:{expires}'.encode(),hashlib.sha256).hexdigest()


@app.get('/styles',dependencies=[Depends(auth)],operation_id='getStyles')
def styles():
    return {'styles':[{'id':s,'modes':['offline','server']} for s in STYLES],
            'limits':{'seconds':120,'frames':3600,'pixel_frames':1500000000,'production_pixel_frames':6000000000,'queued_jobs':MAX_QUEUE,'body_bytes':MAX_BODY},
            'voice':'subtitles or English eSpeak TTS; no voice cloning','webgl':'optional texture compositor'}


@app.get('/templates',dependencies=[Depends(auth)],operation_id='getTemplates')
def templates():
    from education import TEMPLATES,THEMES
    return {'templates':[{'id':k,'description':v} for k,v in TEMPLATES.items()],
            'themes':list(THEMES),'profiles':['preview','production'],
            'accuracy':'Checks layout, arithmetic and numeric scales; factual claims require human/source review.'}


@app.post('/render',status_code=202,dependencies=[Depends(auth)],operation_id='submitFilm')
async def submit(request:Request):
    chunks=[];size=0
    async for chunk in request.stream():
        size+=len(chunk)
        if size>MAX_BODY:raise HTTPException(413,'Film JSON exceeds 64 KiB')
        chunks.append(chunk)
    try:f=validate(json.loads(b''.join(chunks)))
    except (ValueError,TypeError,RecursionError) as e:raise HTTPException(422,str(e))
    expire()
    if used_bytes()>MAX_DISK-JOB_BYTES:raise HTTPException(503,'Artifact storage full; retry after expiry')
    job_id=uuid.uuid4().hex;folder=DATA/job_id
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        n=c.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
        if n>=MAX_QUEUE:raise HTTPException(429,'Queue full; retry later',headers={'Retry-After':'10'})
        folder.mkdir()
        try:
            (folder/'film.json').write_text(json.dumps(f))
            c.execute("INSERT INTO jobs VALUES(?, 'queued', ?, ?, NULL, NULL)",(job_id,time.time(),time.time()))
        except BaseException:shutil.rmtree(folder);raise
    return {'id':job_id,'status':'queued','poll_after_seconds':2}


@app.get('/jobs/{job_id}',dependencies=[Depends(auth)],operation_id='getJob')
def status(job_id:str):
    row=get_job_row(job_id)
    result={'id':job_id,'status':row['status'],'poll_after_seconds':2,'error':row['error']}
    if row['status']=='completed':
        expires=int(time.time())+900
        result.update(json.loads(row['result']))
        result['download_url']=f'{BASE}/jobs/{job_id}/download?expires={expires}&token={signature(job_id,expires)}'
        result['download_expires_at']=expires
    return result


@app.get('/jobs/{job_id}/download',operation_id='downloadFilm')
def download(job_id:str,request:Request,expires:int=0,token:str=''):
    # Signed capability URL for chat download; raw API key never enters URL.
    supplied=request.headers.get('X-API-Key','')
    key_ok=bool(API_KEY) and secrets.compare_digest(supplied.encode(),API_KEY.encode())
    ticket_ok=(time.time()<=expires<=time.time()+901 and hmac.compare_digest(token.encode(),signature(job_id,expires).encode()))
    if not (key_ok or ticket_ok):raise HTTPException(401,'API key or unexpired download ticket required')
    row=get_job_row(job_id)
    if row['status']!='completed':raise HTTPException(409,'Film not complete')
    path=DATA/job_id/'film.mp4'
    if not path.exists():raise HTTPException(410,'Artifact expired')
    return FileResponse(path,media_type='video/mp4',filename='chatreel.mp4')
