"""Offline deterministic film renderer. No network or installation at runtime."""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import wave

ROOT = Path(__file__).resolve().parents[1]
LEGACY_STYLES = ['swiss-motion', 'blueprint', 'chalkboard', 'woodcut', 'pixel-rpg']
STYLES = LEGACY_STYLES + ['studio', 'midnight', 'paper', 'ocean', 'coral', 'violet']
MAX_PIXELS = 1_500_000_000


def capabilities():
    return {**{n: importlib.util.find_spec(m) is not None for n, m in
               [('pillow', 'PIL'), ('numpy', 'numpy'), ('moviepy', 'moviepy'), ('jsonschema', 'jsonschema')]},
            'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
            'tts': False, 'webgl': False, 'bundled_fonts': (ROOT/'renderer-py/assets/fonts/DejaVuSans.ttf').exists()}


def _check(value, spec, path='$'):
    """Validate the deliberately small schema vocabulary without optional packages."""
    typ = spec.get('type')
    ok = {'object': lambda: isinstance(value, dict), 'array': lambda: isinstance(value, list),
          'string': lambda: isinstance(value, str), 'boolean': lambda: isinstance(value, bool),
          'number': lambda: type(value) is int or (type(value) is float and math.isfinite(value)),
          'integer': lambda: type(value) is int}
    if typ and not ok[typ]():
        raise ValueError(f'{path}: expected {typ}')
    if 'enum' in spec and value not in spec['enum']:
        raise ValueError(f'{path}: unsupported value')
    if typ == 'object':
        if len(value)>spec.get('maxProperties',100):raise ValueError(f'{path}: too many properties')
        for k in spec.get('required', []):
            if k not in value:
                raise ValueError(f'{path}: missing {k}')
        for k, v in value.items():
            if k not in spec.get('properties', {}):
                extra=spec.get('additionalProperties')
                if isinstance(extra,dict):_check(v,extra,f'{path}.{k}');continue
                raise ValueError(f'{path}: unknown field {k}')
            _check(v, spec['properties'][k], f'{path}.{k}')
    if typ == 'array':
        if not spec.get('minItems', 0) <= len(value) <= spec.get('maxItems', math.inf):
            raise ValueError(f'{path}: invalid item count')
        for i, v in enumerate(value):
            _check(v, spec['items'], f'{path}[{i}]')
    if typ == 'string':
        try: value.encode('utf-8')
        except UnicodeError: raise ValueError(f'{path}: invalid Unicode')
        if not spec.get('minLength', 0) <= len(value) <= spec.get('maxLength', math.inf):
            raise ValueError(f'{path}: invalid text length')
    if typ in ('integer', 'number'):
        if not spec.get('minimum', -math.inf) <= value <= spec.get('maximum', math.inf):
            raise ValueError(f'{path}: out of range')
        if 'multipleOf' in spec and value % spec['multipleOf']:
            raise ValueError(f'{path}: must be divisible by {spec["multipleOf"]}')


def validate(film):
    schema = json.loads((ROOT / 'film-schema.json').read_text())
    _check(film, schema)
    f = copy.deepcopy(film)
    production=f.get('profile')=='production'
    for k, v in [('width', 1920 if production else 640), ('height', 1080 if production else 360), ('fps', 30 if production else 24), ('seed', 7),
                 ('voice', 'subtitles'), ('webgl', False)]:
        f.setdefault(k, v)
    duration = sum(s['duration'] for s in f['scenes'])
    frames = math.ceil(duration * f['fps'])
    if duration > 120 or frames > 3600 or frames*f['width']*f['height'] > (6_000_000_000 if production else MAX_PIXELS):
        raise ValueError('Film exceeds duration/frame/pixel budget; reduce length, fps or resolution')
    for index,scene in enumerate(f['scenes']):
        if abs(scene['duration']*f['fps']-round(scene['duration']*f['fps']))>1e-6:
            raise ValueError('Scene durations must align to whole video frames')
        if 'template' in scene:
            if scene.get('objects'):raise ValueError('Template scenes use content, not legacy objects')
            if f['webgl']:raise ValueError('Educational templates use shared 2D Canvas/Pillow; set webgl=false')
            if not .5<=f['width']/f['height']<=2:raise ValueError('Template output must be between 1:2 and 2:1 aspect ratio')
            if len(scene.get('narration',''))>scene['duration']*18:raise ValueError('Caption too long for scene; shorten it or extend duration')
            from education import compile_scene
            compile_scene(f,scene,index)
            continue
        if f['style'] not in LEGACY_STYLES:raise ValueError('New themes require an educational template scene')
        if 'content' in scene:raise ValueError('content requires a template')
        if not scene.get('objects'):raise ValueError('Legacy scenes require objects, or choose an educational template')
        for obj in scene['objects']:
            radius = obj.get('size', .1)
            if obj['y']-radius < .24 or obj['y']+radius > .69:
                raise ValueError('Actor overlaps title/caption lane; adjust y or size')
            margin = (.035 if obj.get('motion') == 'drift' else 0) + (.04 if scene.get('camera') == 'pan' else 0)
            edge = radius*f['height']/f['width']*1.06 + margin + .02
            if not edge <= obj['x'] <= 1-edge:
                raise ValueError('Actor may leave frame; adjust x or size')
    for c in f.get('music', {}).get('cues', []):
        if c['time'] >= duration:
            raise ValueError('Music cue must start inside the film')
    return f


@__import__('functools').lru_cache(maxsize=128)
def font(size):
    from PIL import ImageFont
    for p in [str(ROOT/'renderer-py/assets/fonts/DejaVuSans.ttf'), '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
        if Path(p).exists():
            return ImageFont.truetype(p, max(8, int(size)))
    try:
        return ImageFont.load_default(size=max(8, int(size)))
    except TypeError:
        return ImageFont.load_default()


def lines_for(draw, text, width, size, max_lines=3):
    # Break long words too; choose the largest fitting font.
    for n in range(int(size), 7, -1):
        ft = font(n)
        lines, line = [], ''
        for ch in text:
            trial = line + ch
            if draw.textlength(trial, font=ft) > width or ch == '\n':
                lines.append(line.rstrip()); line = '' if ch == '\n' else ch
            else:
                line = trial
        if line:
            lines.append(line.rstrip())
        if len(lines) <= max_lines:
            return lines, ft, n
    raise ValueError('Caption cannot fit; shorten text')


class Scene:
    """A scene's frame is a pure function of local time t, independent of call order."""
    def __init__(self, film, scene, index=0):
        self.film, self.scene, self.index = film, scene, index
        self.plan=None
        if 'template' in scene:
            from education import compile_scene,PreparedScene
            self.plan=compile_scene(film,scene,index)
            self.prepared=PreparedScene(self.plan,film['width'],film['height'])

    def render(self, t):
        if self.plan is not None:
            return self.prepared.render(t)
        from PIL import Image, ImageDraw
        import numpy as np
        f, s = self.film, self.scene
        style = f['style']; pixel = style == 'pixel-rpg'
        w, h = (320, 180) if pixel else (f['width'], f['height'])
        palettes = {'swiss-motion': ('#f2f0ea', '#161616', '#e3472b'),
                    'blueprint': ('#183b75', '#e7f0f9', '#e7f0f9'),
                    'chalkboard': ('#153b32', '#eee7cc', '#e2c96c'),
                    'woodcut': ('#eee4cd', '#171812', '#b85b32'),
                    'pixel-rpg': ('#172444', '#b7d8c8', '#e7aa58')}
        bg, ink, accent = palettes[style]
        im = Image.new('RGB', (w, h), bg); d = ImageDraw.Draw(im)
        rng = np.random.default_rng(f['seed'] + self.index)
        if style in ('blueprint', 'chalkboard', 'woodcut'):
            a = np.asarray(im).astype(np.int16)
            a += rng.integers(-3, 4, (h, w, 1), dtype=np.int16)
            im = Image.fromarray(np.clip(a, 0, 255).astype('uint8')); d = ImageDraw.Draw(im)
        if style == 'swiss-motion':
            for i in range(1, 12):
                x = int(w*(.06 + .88*i/12)); d.line((x, h*.23, x, h*.71), fill='#dedcd5')
            d.line((w*.06, h*.22, w*.94, h*.22), fill=ink, width=2)
            d.text((w*.82, h*.08), f'{self.index+1:02}', font=font(h*.09), fill=ink)
        elif style == 'blueprint':
            for x in range(15, w, max(12, w//24)):
                d.line((x, h*.22, x, h*.7), fill='#254d83')
            for y in range(int(h*.22), int(h*.7), max(12, w//24)):
                d.line((w*.04, y, w*.96, y), fill='#254d83')
            d.rectangle((w*.02, h*.02, w*.98, h*.98), outline=ink)
            d.text((w*.73, h*.68), f'FIG. {self.index+1} / REV 01', font=font(h*.028), fill=ink)
        elif style == 'chalkboard':
            d.rectangle((2, 2, w-3, h-3), outline='#795d3b', width=max(3, w//80))
            d.line((w*.02, h*.94, w*.98, h*.94), fill='#997b53', width=4)
        elif style == 'woodcut':
            d.rectangle((w*.045, h*.23, w*.955, h*.70), fill=ink)
        else:
            for k in range(3):
                y = int(h*(.38+k*.10)); offset = int(t*(3+k*2))%32
                for x in range(-32, w+32, 32):
                    d.polygon([(x-offset,y+25),(x+16-offset,y-8),(x+32-offset,y+25)],fill=['#283d52','#335454','#487561'][k])
            d.rectangle((0, h*.65, w, h*.72), fill='#416757')
        # Actors remain above captions. Camera transforms only actor world.
        for j, obj in enumerate(s['objects']):
            clock = math.floor(t*8)/8 if pixel else t
            x, y = obj['x']*w, obj['y']*h
            radius = obj.get('size', .1)*h
            motion = obj.get('motion', 'still')
            if motion == 'drift': x += math.sin(clock*1.3)*w*.035
            if motion == 'pulse': radius *= 1+.08*math.sin(clock*3)
            camera = s.get('camera', 'locked')
            z = 1 + .06*min(t/s['duration'], 1) if camera == 'push' else 1
            x = w/2+(x-w/2)*z; y = h*.46+(y-h*.46)*z; radius *= z
            if camera == 'pan': x -= w*.04*t/s['duration']
            colour = accent if obj.get('accent') else ink
            if pixel: x,y,radius = round(x),round(y),round(radius)
            # Full actor masks, clipped by a style-native draw-on wipe.
            layer = Image.new('RGBA', (w,h)); ld=ImageDraw.Draw(layer)
            shape = obj['shape']; box=(x-radius,y-radius,x+radius,y+radius)
            outline_only = style in ('blueprint','chalkboard')
            kw = {'outline':colour,'width':max(1,int(h*.006))} if outline_only else {'fill':colour}
            if style == 'woodcut':
                kw = {'fill':ink, 'outline':accent if obj.get('accent') else bg, 'width':max(1,int(h*.006))}
            if shape == 'circle': ld.ellipse(box,**kw)
            elif shape == 'box': ld.rectangle(box,**kw)
            elif shape == 'triangle':
                points=[(x,y-radius),(x+radius,y+radius),(x-radius,y+radius),(x,y-radius)]
                if outline_only:ld.line(points,fill=colour,width=max(1,int(h*.006)))
                else:
                    ld.polygon(points,fill=ink if style=='woodcut' else colour)
                    if style=='woodcut':ld.line(points,fill=accent if obj.get('accent') else bg,width=max(1,int(h*.006)))
            else:
                ld.ellipse((x-radius*.3,y-radius,x+radius*.3,y-radius*.4),**kw)
                ld.rectangle((x-radius*.35,y-radius*.35,x+radius*.35,y+radius*.4),**kw)
                ld.line((x-radius*.2,y+radius*.35,x-radius*.4,y+radius),fill=colour,width=max(2,int(radius*.2)))
                ld.line((x+radius*.2,y+radius*.35,x+radius*.4,y+radius),fill=colour,width=max(2,int(radius*.2)))
            if style == 'woodcut':
                # Cuts wrap the form: curved gouges carved out of black ink.
                for k in range(10):
                    rr=radius*(.4+k*.055)
                    cut_colour=accent if obj.get('accent') else bg
                    if shape == 'box':
                        yy=y-radius+radius*.12*k
                        ld.line((x-radius*.88,yy,x-radius*.15,yy+radius*.4),fill=cut_colour,width=max(1,int(h*.005)))
                    else:
                        ld.arc((x-rr,y-rr,x+rr,y+rr), 200, 340,fill=cut_colour,width=max(1,int(h*.005)))
            if style == 'chalkboard':
                pixels=np.array(layer)
                tooth=rng.random((h,w))<.16
                pixels[tooth,3]=pixels[tooth,3]//3
                layer=Image.fromarray(pixels)
            p = min(1, max(0,(t-j*.035)/.65))
            # Swiss snaps, technical/chalk draw-on, wood relief; no alpha fades.
            if style == 'swiss-motion': p = p*p*(3-2*p)
            cut = int(x-radius+2*radius*p)
            if p < 1: layer.paste((0,0,0,0),(max(0,cut),0,w,h))
            im.paste(layer,(0,0),layer); d=ImageDraw.Draw(im)
            if style == 'blueprint' and p == 1:
                yy=y+radius+8
                d.line((x-radius, yy, x+radius, yy),fill=ink)
                for xx in [x-radius,x+radius]:d.line((xx,yy-4,xx,yy+4),fill=ink)
                d.text((x-radius, yy+2),f'{j+1:02} / {int(radius*2)}',font=font(h*.026),fill=ink)
        # Text never follows camera. Dedicated caption lane.
        d=ImageDraw.Draw(im)
        title_lines, ft, fs = lines_for(d,s['title'],w*.70,h*.07,2)
        for k, line in enumerate(title_lines): d.text((w*.07,h*.065+k*fs*1.15),line,font=ft,fill=ink)
        caption=s.get('narration','')
        if caption:
            if pixel: d.rectangle((10,133,310,174),fill='#172444',outline=ink,width=2)
            elif style == 'blueprint':d.rectangle((w*.055,h*.76,w*.945,h*.93),outline=ink)
            elif style not in ('woodcut','swiss-motion'):d.line((w*.07,h*.75,w*.93,h*.75),fill=ink)
            cap_lines, ft, fs = lines_for(d,caption,w*.82,h*.048,3)
            top=h*.78 if not pixel else 139
            for k,line in enumerate(cap_lines):d.text((w*.09,top+k*fs*1.15),line,font=ft,fill=ink)
        if pixel: im=im.resize((f['width'],f['height']),Image.Resampling.NEAREST)
        return im


def frame_at(f, t):
    start=0
    for i,s in enumerate(f['scenes']):
        if t < start+s['duration'] or i == len(f['scenes'])-1:
            return Scene(f,s,i).render(max(0,t-start))
        start+=s['duration']


class FilmRenderer:
    def __init__(self,film):
        self.film=film;self.scenes=[Scene(film,s,i) for i,s in enumerate(film['scenes'])]
    def frame(self,t):
        start=0
        for i,s in enumerate(self.film['scenes']):
            if t<start+s['duration'] or i==len(self.scenes)-1:return self.scenes[i].render(max(0,t-start))
            start+=s['duration']
    def export_plans(self,out):
        from education import svg_frame
        report=[]
        for i,scene in enumerate(self.scenes):
            if scene.plan:
                (out/f'scene-{i+1:02}.svg').write_text(svg_frame(scene.plan,scene.scene['duration']-.01))
                report.append(scene.plan.metrics)
        if report:
            (out/'scene-metrics.json').write_text(json.dumps(report,indent=2))
            sources=[{'scene':i+1,'template':s.get('template'),'source':s.get('content',{}).get('source'),
                'data_kind':s.get('content',{}).get('data_kind','illustrative'),'verification':'source/factual review required'} for i,s in enumerate(self.film['scenes']) if 'template' in s]
            (out/'SOURCES.json').write_text(json.dumps(sources,indent=2))


def score(f, sample_rate=24000):
    if any('template' in scene for scene in f['scenes']):
        from audio import arranged_score
        return arranged_score(f,sample_rate)
    import numpy as np
    dur=sum(s['duration'] for s in f['scenes']); n=round(dur*sample_rate)
    a=np.zeros(n,dtype=np.float64); music=f.get('music',{})
    if not music.get('enabled',True):return a
    beat=60/music.get('bpm',100)
    events=[{'time':float(t),'note':[60,64,67,72][i%4],'duration':min(.4,beat*.7)}
            for i,t in enumerate(np.arange(0,dur,beat))]+music.get('cues',[])
    for e in events:
        start=round(e['time']*sample_rate); length=min(n-start,round(e.get('duration',.4)*sample_rate))
        if length<=0:continue
        t=np.arange(length)/sample_rate; hz=440*2**((e['note']-69)/12)
        if f['style']=='pixel-rpg':v=np.where(np.sin(2*np.pi*hz*t)>.4,1.,-1.)*.6
        elif f['style']=='woodcut':v=np.sin(2*np.pi*hz*t)+.3*np.sin(2*np.pi*hz*2.71*t)
        elif f['style']=='blueprint':v=np.sin(2*np.pi*hz*t)+.25*np.sin(2*np.pi*hz*3*t)
        elif f['style']=='chalkboard':v=np.sin(2*np.pi*hz*t)*np.exp(-t*8)
        else:v=np.sin(2*np.pi*hz*t)+.2*np.sin(2*np.pi*hz*2*t)
        env=np.minimum(t/.015,1)*np.minimum((length/sample_rate-t)/.04,1)*np.exp(-t*3)
        a[start:start+length]+=v*env*music.get('gain',.15)
    return np.clip(a,-.85,.85)


def write_wav(path, audio, rate=24000):
    import numpy as np
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,rate,0,'NONE','not compressed'))
        w.writeframes((np.clip(audio,-.98,.98)*32767).astype('<i2').tobytes())


def read_voice(path, duration, work, ffmpeg):
    import numpy as np
    target=Path(work)/'voice-decoded.wav'
    if ffmpeg:
        subprocess.run([ffmpeg,'-v','error','-y','-i',str(path),'-t',str(duration),'-ac','1','-ar','24000',str(target)],check=True,timeout=60)
    else:target=Path(path)
    with wave.open(str(target),'rb') as w:
        if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getframerate()!=24000:
            raise ValueError('Without ffmpeg voice must be mono PCM16 WAV at 24000 Hz')
        v=np.frombuffer(w.readframes(round(duration*24000)),dtype='<i2').astype(float)/32768
    return v


def subtitle_files(f,out):
    def stamp(t):
        ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    start=0; rows=[]
    for s in f['scenes']:
        if s.get('narration'):rows.append(f'{len(rows)+1}\n{stamp(start)} --> {stamp(start+s["duration"])}\n{s["narration"]}\n')
        start+=s['duration']
    (out/'film.srt').write_text('\n'.join(rows))


def normalize_audio(ff,source,target,duration):
    """Two-pass EBU R128 normalization. Silent audio is handled explicitly."""
    import re
    measure=subprocess.run([ff,'-hide_banner','-nostats','-i',str(source),'-af',
        'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True,timeout=90)
    match=re.search(r'\{\s*"input_i".*?\}',measure.stderr,re.S)
    if not match:raise RuntimeError('Cannot measure audio loudness')
    values=json.loads(match.group())
    keys=['input_i','input_tp','input_lra','input_thresh','target_offset']
    finite=all(math.isfinite(float(values[k])) for k in keys)
    af=('loudnorm=I=-14:TP=-1.5:LRA=11:measured_I='+values['input_i']+
        ':measured_TP='+values['input_tp']+':measured_LRA='+values['input_lra']+
        ':measured_thresh='+values['input_thresh']+':offset='+values['target_offset']+':linear=true') if finite else 'anull'
    subprocess.run([ff,'-v','error','-y','-i',str(source),'-af',af+',apad=whole_dur='+str(duration),
        '-t',str(duration),'-ar','48000',str(target)],check=True,timeout=90)
    return {'target_lufs':-14,'target_true_peak_db':-1.5,'input_lufs':float(values['input_i']) if finite else None,'silent':not finite}


def inspect_output(path,f):
    probe=capabilities()['ffprobe']
    if not probe:return {'status':'unverified','reason':'ffprobe unavailable'}
    data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_format','-show_streams','-of','json',str(path)],timeout=90))
    video=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    count=round(sum(s['duration'] for s in f['scenes'])*f['fps'])
    if not video or not audio:raise RuntimeError('Encoded output lacks video or audio')
    if (video['width'],video['height'])!=(f['width'],f['height']):raise RuntimeError('Encoded output resolution changed')
    if int(video.get('nb_read_frames',video.get('nb_frames',0)))!=count:raise RuntimeError('Encoded output frame count mismatch')
    duration=sum(s['duration'] for s in f['scenes'])
    if abs(float(data['format']['duration'])-duration)>.1:raise RuntimeError('Encoded output duration mismatch')
    return {'status':'passed','frames':count,'duration':duration,'width':video['width'],'height':video['height'],
            'codec':video['codec_name'],'pixel_format':video['pix_fmt'],'audio_codec':audio['codec_name'],
            'color_space':video.get('color_space'),'fps':video['avg_frame_rate']}


def encode_frames(f, frames, out, audio):
    ff=capabilities()['ffmpeg']; dur=sum(s['duration'] for s in f['scenes'])
    if ff:
        target=out/'film.mp4'
        normalized=out/'master.wav'
        audio_report=normalize_audio(ff,audio,normalized,dur)
        with tempfile.TemporaryFile() as err:
            proc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{f["width"]}x{f["height"]}',
                 '-r',str(f['fps']),'-i','pipe:0','-i',str(normalized),'-t',str(dur),'-map','0:v:0','-map','1:a:0',
                 '-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
                 '-c:v','libx264','-threads','2','-preset','medium','-crf','18' if f.get('profile')=='production' else '20',
                 '-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
                 '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(target)],stdin=subprocess.PIPE,stderr=err)
            try:
                written=0
                for im in frames:
                    if im.size!=(f['width'],f['height']):raise RuntimeError('Renderer returned an unexpected frame size')
                    proc.stdin.write(im.convert('RGB').tobytes());written+=1
                if written!=round(dur*f['fps']):raise RuntimeError('Renderer returned an unexpected frame count')
                proc.stdin.close()
                if proc.wait(timeout=60):
                    err.seek(0);raise RuntimeError(err.read().decode()[-2000:])
            except BaseException:
                proc.kill();proc.wait();target.unlink(missing_ok=True);raise
        (out/'quality.json').write_text(json.dumps({'encoding':inspect_output(target,f),'audio':audio_report},indent=2))
        return target
    if capabilities()['moviepy']:
        try:from moviepy import VideoClip, AudioFileClip
        except ImportError:from moviepy.editor import VideoClip, AudioFileClip
        import numpy as np
        clip=VideoClip(lambda t:np.asarray(frame_at(f,t)),duration=dur)
        ac=AudioFileClip(str(audio))
        clip=clip.with_audio(ac) if hasattr(clip,'with_audio') else clip.set_audio(ac)
        try:clip.write_videofile(str(out/'film.mp4'),fps=f['fps'],codec='libx264',audio_codec='aac',logger=None)
        finally:clip.close();ac.close()
        (out/'quality.json').write_text(json.dumps({'encoding':inspect_output(out/'film.mp4',f),'audio':{'normalization':'not measured in MoviePy fallback'}},indent=2))
        return out/'film.mp4'
    folder=out/'frames';folder.mkdir(exist_ok=True)
    for i,im in enumerate(frames):im.save(folder/f'{i:06}.png')
    return None


def render_film(film, output_dir, voice_path=None):
    caps=capabilities()
    if not caps['pillow'] or not caps['numpy']:
        raise RuntimeError(f'Pillow and numpy are required; available: {caps}')
    import numpy as np
    from PIL import Image
    f=validate(film);out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    dur=sum(s['duration'] for s in f['scenes']);warnings=[]
    for name in ('film.mp4','quality.json','scene-metrics.json'):(out/name).unlink(missing_ok=True)
    if f['voice']=='tts':warnings.append('Offline TTS unavailable: rendered subtitles instead')
    if f['webgl']:warnings.append('Offline WebGL unavailable: rendered 2D instead')
    audio=score(f)
    if voice_path:
        v=read_voice(voice_path,dur,out,caps['ffmpeg']);n=min(len(audio),len(v))
        from audio import mix_voice
        audio=mix_voice(audio,v[:n])
    write_wav(out/'mix.wav',audio)
    subtitle_files(f,out)
    renderer=FilmRenderer(f);renderer.export_plans(out)
    frames=(renderer.frame(i/f['fps']) for i in range(round(dur*f['fps'])))
    try:
        mp4=encode_frames(f,frames,out,out/'mix.wav')
    except (RuntimeError, OSError, ImportError, subprocess.SubprocessError) as error:
        warnings.append(f'Encoder failed ({type(error).__name__}): exported frames instead')
        (out/'film.mp4').unlink(missing_ok=True)
        folder=out/'frames';folder.mkdir(exist_ok=True)
        for i in range(round(dur*f['fps'])):renderer.frame(i/f['fps']).save(folder/f'{i:06}.png')
        mp4=None
    if not mp4:warnings.append('No MP4 encoder: exported PNG sequence, WAV and SRT')
    sheet=Image.new('RGB',(f['width']*3,f['height']))
    for i,t in enumerate([.1,dur*.5,max(0,dur-.1)]):sheet.paste(renderer.frame(t),(i*f['width'],0))
    sheet.save(out/'contact-sheet.jpg');renderer.frame(dur*.5).save(out/'poster.png')
    (out/'film.json').write_text(json.dumps(f,indent=2))
    (out/'CREDITS.txt').write_text('Style interpretation adapted from Lemomo/LemoLab: https://github.com/lemomo-ai/lemo-opuscar\nMIT code/docs; CC BY 4.0 style adaptations. New procedural graphics and original synthesized score.\nFont: bundled DejaVu Sans; see licenses/DEJAVU-FONTS.txt. No demo media used.\n'+('Voice: user-uploaded recording.\n' if voice_path else 'Voice: none (subtitles).\n'))
    for i,scene in enumerate(renderer.scenes):
        if scene.plan and scene.plan.metrics['recommended_duration']>scene.scene['duration']:
            warnings.append(f'Scene {i+1}: allow about {scene.plan.metrics["recommended_duration"]}s to read; current duration is {scene.scene["duration"]}s')
    result={'mp4':str(mp4) if mp4 else None,'duration':dur,'warnings':warnings,'capabilities':caps}
    (out/'result.json').write_text(json.dumps(result,indent=2));return result


def main():
    p=argparse.ArgumentParser(description='Model-free educational video renderer')
    p.add_argument('script',nargs='?');p.add_argument('--out',default='artifacts/offline');p.add_argument('--voice')
    p.add_argument('--capabilities',action='store_true');p.add_argument('--templates',action='store_true')
    p.add_argument('--preflight',action='store_true');p.add_argument('--template');p.add_argument('--theme',choices=STYLES)
    p.add_argument('--profile',choices=['preview','production']);p.add_argument('--aspect',choices=['wide','portrait','square'])
    a=p.parse_args()
    if a.templates:
        from education import TEMPLATES,THEMES
        print(json.dumps({'templates':TEMPLATES,'themes':list(THEMES)},indent=2));return
    if a.capabilities:print(json.dumps(capabilities(),indent=2));return
    if a.template:
        from education import TEMPLATES
        if a.template not in TEMPLATES:p.error('Unknown template; use --templates to list choices')
        if a.script:p.error('Choose a script or --template, not both')
        film=json.loads((ROOT/'templates'/f'{a.template}.json').read_text())
    elif a.script:film=json.loads(Path(a.script).read_text())
    else:p.error('Provide a film JSON or --template NAME')
    if a.theme:film['style']=a.theme
    if a.profile:
        film['profile']=a.profile
        film.update(width=1920 if a.profile=='production' else 1280,height=1080 if a.profile=='production' else 720,fps=30 if a.profile=='production' else 24)
    if a.aspect:
        short=1080 if film.get('profile')=='production' else 720
        if a.aspect=='portrait':film.update(width=short,height=short*16//9)
        elif a.aspect=='square':film.update(width=short,height=short)
        else:film.update(width=short*16//9,height=short)
    film=validate(film)
    if a.preflight:
        renderer=FilmRenderer(film)
        print(json.dumps({'status':'passed','duration':sum(s['duration'] for s in film['scenes']),
            'scenes':[{'template':s.scene.get('template'),'recommended_duration':s.plan.metrics['recommended_duration'] if s.plan else None} for s in renderer.scenes]},indent=2));return
    print(json.dumps(render_film(film,a.out,a.voice),indent=2))


if __name__=='__main__':main()
