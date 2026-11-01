"""Render and audit every educational template; defaults keep review affordable."""
import argparse
import json
from pathlib import Path
import sys
import time
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from render import render_film,validate,FilmRenderer
from education import font
p=argparse.ArgumentParser();p.add_argument('--backend',choices=['python','canvas'],default='python');p.add_argument('--width',type=int,default=640);p.add_argument('--fps',type=int,default=12);p.add_argument('--out');p.add_argument('--clip-seconds',type=int,default=5);args=p.parse_args()
out=Path(args.out) if args.out else ROOT/'artifacts'/('education-final-'+args.backend);out.mkdir(parents=True,exist_ok=True)
films=[p for p in sorted((ROOT/'templates').glob('*.json')) if p.name!='index.json'];rows=[]
sheet=Image.new('RGB',(960,210*((len(films)+2)//3)),'#edf1f5');draw=ImageDraw.Draw(sheet)
for i,path in enumerate(films):
    film=json.loads(path.read_text());film.update(width=args.width,height=args.width*9//16,fps=args.fps)
    film['scenes'][0]['duration']=args.clip_seconds
    film=validate(film);folder=out/path.stem;folder.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    if args.backend=='python':result=render_film(film,folder)
    else:
        sys.path.insert(0,str(ROOT));from server.worker import render_job
        (folder/'film.json').write_text(json.dumps(film,indent=2));result=render_job(film,folder)
    if not (folder/'film.mp4').exists():raise RuntimeError(f'No MP4 for {path.stem}: {result}')
    renderer=FilmRenderer(film);im=renderer.frame(3);im.thumbnail((320,180))
    if args.backend=='canvas':im=Image.open(folder/'poster.png');im.thumbnail((320,180))
    x=(i%3)*320;y=(i//3)*210;sheet.paste(im,(x,y+25));draw.text((x+6,y+3),path.stem,fill='#182b3a',font=font(15))
    rows.append({'template':path.stem,'backend':args.backend,'seconds_to_render':round(time.monotonic()-start,2),'result':result})
    print(path.stem,'rendered',round(time.monotonic()-start,2),'s',flush=True)
sheet.save(out/'gallery.jpg',quality=92);(out/'render-report.json').write_text(json.dumps(rows,indent=2))
