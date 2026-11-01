"""Server integration tests perform real five-second Chromium renders.
Run with CHROMIUM_EXECUTABLE set if using a system browser. Requires eSpeak.
"""
import copy
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from server import app as module

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        module.DATA=Path(cls.temp.name)
        module.API_KEY=secrets.token_urlsafe(32)
        cls.headers={'X-API-Key':module.API_KEY}
        cls.client=TestClient(module.app)
        cls.client.__enter__()
        cls.film=json.loads((ROOT/'examples/film.json').read_text())
    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None,None,None);cls.temp.cleanup()
    def wait(self,job):
        deadline=time.monotonic()+90
        while time.monotonic()<deadline:
            r=self.client.get('/jobs/'+job,headers=self.headers).json()
            if r['status'] in ('completed','failed'):return r
            time.sleep(.1)
        self.fail('Job failed to finish')
    def test_auth_validation_and_body_limits(self):
        self.assertEqual(self.client.get('/styles').status_code,401)
        self.assertEqual(self.client.get('/styles',headers=self.headers).status_code,200)
        self.assertEqual(self.client.get('/jobs/../../etc/passwd',headers=self.headers).status_code,404)
        self.assertEqual(self.client.post('/render',headers=self.headers,json={'title':'bad'}).status_code,422)
        self.assertEqual(self.client.post('/render',headers=self.headers,content=b'x'*65537).status_code,413)
        self.assertEqual(self.client.get('/jobs/'+'a'*32+'/download').status_code,401)
    def test_real_browser_render_every_style_and_signed_download(self):
        from render import STYLES
        import shutil
        artifacts=ROOT/'artifacts/server-validation';artifacts.mkdir(parents=True,exist_ok=True)
        for style in STYLES:
            film=copy.deepcopy(self.film);film['style']=style
            film['webgl']=style=='woodcut';film['voice']='tts' if style=='blueprint' else 'subtitles'
            response=self.client.post('/render',headers=self.headers,json=film)
            self.assertEqual(response.status_code,202,response.text)
            job=response.json()['id'];result=self.wait(job)
            if result['status']=='failed':
                log=(module.DATA/job/'worker.log').read_text();self.fail(log[-4000:])
            self.assertEqual(result['frames'],120)
            url=result['download_url'].split(module.BASE)[1]
            download=self.client.get(url)
            self.assertEqual(download.status_code,200)
            self.assertEqual(download.headers['content-type'],'video/mp4')
            self.assertGreater(len(download.content),10000)
            self.assertEqual(self.client.get(url.replace('token=','token=x')).status_code,401)
            self.assertEqual(self.client.get('/jobs/'+job+'/download',headers=self.headers).status_code,200)
            target=artifacts/style;target.mkdir(exist_ok=True)
            for filename in ['film.json','film.mp4','film.srt','contact-sheet.jpg','poster.png','CREDITS.txt','result.json']:
                shutil.copy2(module.DATA/job/filename,target/filename)
            print('Validated server',style,result['backend'],flush=True)
    def test_queue_cap_and_expired_ticket(self):
        # Reserve all slots synchronously; no background subprocess can claim missing data.
        now=time.time()
        with module.db() as c:
            for i in range(module.MAX_QUEUE):c.execute("INSERT INTO jobs VALUES(?, 'running', ?, ?, NULL, NULL)",(f'reserved{i}',now,now))
        try:self.assertEqual(self.client.post('/render',json=self.film,headers=self.headers).status_code,429)
        finally:module.change("DELETE FROM jobs WHERE id LIKE 'reserved%'")
        job='b'*32;expires=int(time.time())-1
        self.assertEqual(self.client.get(f'/jobs/{job}/download?expires={expires}&token={module.signature(job,expires)}').status_code,401)
    def test_hard_deadline_marks_failed(self):
        from unittest.mock import patch
        with patch.object(module,'TIMEOUT',0):
            job=self.client.post('/render',headers=self.headers,json=self.film).json()['id']
            result=self.wait(job)
        self.assertEqual(result['status'],'failed')
        self.assertIn('time limit',result['error'])
        self.assertFalse((module.DATA/job/'film.mp4').exists())

    def test_speech_overflow_fails_without_download(self):
        film=copy.deepcopy(self.film);film['voice']='tts';film['scenes'][0]['duration']=1
        film['music']={'enabled':False}
        job=self.client.post('/render',headers=self.headers,json=film).json()['id']
        result=self.wait(job);self.assertEqual(result['status'],'failed')
        self.assertIn('speech exceeds',(module.DATA/job/'worker.log').read_text())
        self.assertEqual(self.client.get('/jobs/'+job+'/download',headers=self.headers).status_code,409)

if __name__=='__main__':unittest.main()
