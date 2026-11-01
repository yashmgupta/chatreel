"""Inspect encoded outputs, not just pre-encode frame buffers."""
from pathlib import Path
import io
import json
import re
import subprocess
import sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from render import LEGACY_STYLES as STYLES,font
report=[]
for mode in ['offline','server']:
    sheet=Image.new('RGB',(960,220*len(STYLES)),'white')
    for row,style in enumerate(STYLES):
        directory=ROOT/'artifacts'/f'{mode}-validation'/style;mp4=directory/'film.mp4'
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(mp4)]))
        duration=float(probe['format']['duration']);streams=probe['streams'];v=next(s for s in streams if s['codec_type']=='video')
        assert abs(duration-5)<.15 and int(v['nb_frames'])==120
        assert any(s['codec_type']=='audio' for s in streams)
        rgb=[]
        for col,t in enumerate([.1,2.5,4.8]):
            frame=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(mp4),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'])
            im=Image.open(io.BytesIO(frame)).convert('RGB');a=np.asarray(im)
            assert a.std()>10 and np.isfinite(a).all()
            rgb.append(a)
            im.thumbnail((320,180));sheet.paste(im,(320*col,220*row+25))
        assert not np.array_equal(rgb[0],rgb[1])
        log=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(mp4),'-vf','blackdetect=d=0.1:pix_th=0.02','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True).stderr
        assert 'black_start:' not in log
        loudness=re.findall(r'I:\s+(-?[\d.]+) LUFS',log)[-1]
        report.append({'mode':mode,'style':style,'duration':duration,'frames':int(v['nb_frames']),'video_codec':v['codec_name'],'integrated_lufs':float(loudness),'black_intervals':0,'representative_frames':'passed nonblank/finite/motion checks'})
        ImageDraw.Draw(sheet).text((8,220*row+3),style,fill='black',font=font(15))
    sheet.save(ROOT/'artifacts'/f'{mode}-decoded-styles.jpg')
(ROOT/'artifacts/inspection.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
