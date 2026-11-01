"""Produce five offline clips and a labelled visual review sheet."""
from pathlib import Path
import json
import sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from render import STYLES,render_film,font
f=json.loads((ROOT/'examples/film.json').read_text())
sheet=Image.new('RGB',(960,230*len(STYLES)),'white')
for row,style in enumerate(STYLES):
    script={**f,'style':style}
    out=ROOT/'artifacts/offline-validation'/style
    result=render_film(script,out)
    ImageDraw.Draw(sheet).text((8,row*230+3),style,fill='black',font=font(16))
    im=Image.open(out/'contact-sheet.jpg');im.thumbnail((960,180))
    sheet.paste(im,(0,row*230+30))
    print(style,result['duration'],result['mp4'],flush=True)
sheet.save(ROOT/'artifacts/offline-styles.jpg')
