"""Subprocess entrypoint: bounded by the parent worker's hard deadline."""
import base64
import io
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderer-py'))
from render import validate, score, write_wav, read_voice, subtitle_files, encode_frames


def render_job(film, out):
    import numpy as np
    from PIL import Image
    from playwright.sync_api import sync_playwright
    f=validate(film);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    duration=sum(s['duration'] for s in f['scenes']);audio=score(f)
    if f['voice']=='tts':
        engine=shutil.which('espeak-ng') or shutil.which('espeak')
        if not engine:raise RuntimeError('TTS requested but espeak-ng is not installed')
        start=0
        for i,s in enumerate(f['scenes']):
            if s.get('narration'):
                voice=out/f'voice-{i}.wav'
                subprocess.run([engine,'-v','en-us','-s','155','-w',str(voice),'--stdin'],input=s['narration'].encode(),check=True,timeout=30)
                with wave.open(str(voice)) as w: vd=w.getnframes()/w.getframerate()
                if vd>s['duration']-.15:raise ValueError(f'Scene {i+1} speech exceeds its duration; shorten narration')
                v=read_voice(voice,duration,out,shutil.which('ffmpeg'))
                offset=round(start*24000);n=min(len(v),len(audio)-offset)
                from audio import mix_voice
                audio=mix_voice(audio,v[:n],offset)
            start+=s['duration']
    write_wav(out/'mix.wav',audio);subtitle_files(f,out)
    pictures=[]
    from render import FilmRenderer
    from education import evaluated_ops
    renderer=FilmRenderer(f);renderer.export_plans(out)
    with sync_playwright() as p:
        # Production retains Chromium's sandbox. Host must support user namespaces.
        exe=__import__('os').environ.get('CHROMIUM_EXECUTABLE') or None
        browser=p.chromium.launch(executable_path=exe,headless=True,chromium_sandbox=True,
                                 args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        try:
            page=browser.new_page(viewport={'width':f['width'],'height':f['height']},device_scale_factor=1)
            page.route('**/*',lambda route:route.abort())
            page.set_content('<html><body style="margin:0;overflow:hidden"><canvas id="film"></canvas></body></html>')
            page.add_script_tag(content=(ROOT/'server/scene.js').read_text())
            page.add_script_tag(content=(ROOT/'server/display-list.js').read_text())
            for bold in (False,True,'mono'):
                name='DejaVuSansMono.ttf' if bold=='mono' else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
                data=base64.b64encode((ROOT/'renderer-py/assets/fonts'/name).read_bytes()).decode()
                page.evaluate('async ({data,weight,family})=>{const font=new FontFace(family,`url(data:font/ttf;base64,${data})`,{weight});await font.load();document.fonts.add(font);}',{'data':data,'weight':'700' if bold is True else '400','family':'ChatreelMono' if bold=='mono' else 'Chatreel'})
            active=None
            count=math.ceil(duration*f['fps'])
            def frames():
                nonlocal active
                for i in range(count):
                    global_time=i/f['fps'];start=0;scene_index=0
                    for j,scene in enumerate(f['scenes']):
                        scene_index=j
                        if global_time<start+scene['duration'] or j==len(f['scenes'])-1:break
                        start+=scene['duration']
                    plan=renderer.scenes[scene_index].plan
                    backend='display' if plan else 'legacy'
                    if (backend,scene_index)!=active:
                        # Reset the canvas when switching between legacy 2D/WebGL and shared scenes.
                        page.evaluate('()=>{document.getElementById("film").remove();const c=document.createElement("canvas");c.id="film";document.body.appendChild(c);}')
                        if plan:page.evaluate('(args)=>window.initDisplayList(args)',{'width':f['width'],'height':f['height'],'designWidth':plan.width,'designHeight':plan.height})
                        else:page.evaluate('(f)=>window.initFilm(f)',f)
                        active=(backend,scene_index)
                    if plan:page.evaluate('(ops)=>window.drawDisplayList(ops)',evaluated_ops(plan,global_time-start))
                    else:page.evaluate('(t)=>window.render(t)',global_time)
                    im=Image.open(io.BytesIO(page.screenshot(type='png'))).convert('RGB')
                    if i in [0,count//2,count-1]:pictures.append(im.copy())
                    yield im
            mp4=encode_frames(f,frames(),out,out/'mix.wav')
            if not mp4:raise RuntimeError('ffmpeg required on the server')
        finally:browser.close()
    sheet=Image.new('RGB',(f['width']*3,f['height']))
    for i,im in enumerate(pictures):sheet.paste(im,(i*f['width'],0))
    sheet.save(out/'contact-sheet.jpg');pictures[1].save(out/'poster.png')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(mp4)]))
    if abs(float(probe['format']['duration'])-duration)>.15:raise RuntimeError('Encoded duration mismatch')
    if {s['codec_type'] for s in probe['streams']}!={'audio','video'}:raise RuntimeError('Missing output streams')
    (out/'CREDITS.txt').write_text('Style adapted from Lemomo/LemoLab, https://github.com/lemomo-ai/lemo-opuscar\nMIT code/docs, CC BY 4.0 adapted style knowledge. No upstream demo media.\nOriginal procedural music; bundled DejaVu Sans (Bitstream Vera license, see licenses/DEJAVU-FONTS.txt).\nVoice: '+('eSpeak (GPL engine; generated speech is not engine code).\n' if f['voice']=='tts' else 'none (captions).\n'))
    warnings=[]
    for i,scene in enumerate(renderer.scenes):
        if scene.plan and scene.plan.metrics['recommended_duration']>scene.scene['duration']:
            warnings.append(f'Scene {i+1}: consider {scene.plan.metrics["recommended_duration"]}s for reading')
    return {'warnings':warnings,'duration':duration,'frames':count,'backend':'chromium-webgl' if f['webgl'] else 'chromium-shared-canvas' if any('template' in s for s in f['scenes']) else 'chromium-canvas'}


if __name__=='__main__':
    folder=Path(sys.argv[1]);result=render_job(json.loads((folder/'film.json').read_text()),folder)
    (folder/'result.json').write_text(json.dumps(result))
