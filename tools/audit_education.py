"""Audit decoded MP4s, compare backends, and preserve inspectable evidence."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from education import TEMPLATES,font

def frame(path,t,width=640):
    data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-vf',f'scale={width}:-1','-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'])
    return Image.open(io.BytesIO(data)).convert('RGB')

rows=[];sheet=Image.new('RGB',(960,210*6),'#edf1f5');draw=ImageDraw.Draw(sheet)
for i,name in enumerate(sorted(TEMPLATES)):
    captures={};entry={'template':name,'outputs':{}}
    for backend in ('python','canvas'):
        folder=ROOT/'artifacts'/f'education-final-{backend}'/name
        clip=folder/'film.mp4'
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',str(clip)]))
        v=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert int(v['nb_read_frames'])==60 and (v['width'],v['height'])==(640,360)
        assert abs(float(probe['format']['duration'])-5)<.1
        assert any(s['codec_type']=='audio' for s in probe['streams'])
        before=frame(clip,.2);middle=frame(clip,3);last=frame(clip,4.8)
        for im in (before,middle,last):assert np.asarray(im).std()>8
        assert not np.array_equal(np.asarray(before),np.asarray(middle))
        log=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(clip),'-vf','blackdetect=d=0.2:pix_th=0.02','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True).stderr
        assert 'black_start:' not in log
        lufs=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',log)[-1]);peak=float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',log)[-1])
        entry['outputs'][backend]={'duration':float(probe['format']['duration']),'frames':int(v['nb_read_frames']),'resolution':[v['width'],v['height']],'integrated_lufs':lufs,'true_peak_dbfs':peak,'black_intervals':0,'codec':v['codec_name'],'color_space':v.get('color_space')}
        captures[backend]=middle
    diff=float(np.mean(np.abs(np.asarray(captures['python']).astype(float)-np.asarray(captures['canvas']).astype(float))))
    entry['backend_rgb_mean_absolute_difference']=round(diff,3)
    # Text rasterization can differ even with identical commands/fonts; this is a regression threshold, not pixel equality.
    assert diff<8,(name,diff)
    rows.append(entry)
    thumb=captures['canvas'].copy();thumb.thumbnail((320,180));x=(i%3)*320;y=(i//3)*210;sheet.paste(thumb,(x,y+25));draw.text((x+6,y+3),name,fill='#182b3a',font=font(15))
report=ROOT/'artifacts/education-audit.json';report.write_text(json.dumps(rows,indent=2));sheet.save(ROOT/'artifacts/education-decoded-gallery.jpg',quality=92)
print('Audited',len(rows)*2,'encoded MP4s; maximum backend RGB MAE',max(r['backend_rgb_mean_absolute_difference'] for r in rows),flush=True)
print('LUFS range',min(o['integrated_lufs'] for r in rows for o in r['outputs'].values()),max(o['integrated_lufs'] for r in rows for o in r['outputs'].values()))
