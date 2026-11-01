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
STYLES = ['swiss-motion', 'blueprint', 'chalkboard', 'woodcut', 'pixel-rpg']
MAX_PIXELS = 1_500_000_000


def capabilities():
    return {**{n: importlib.util.find_spec(m) is not None for n, m in
               [('pillow', 'PIL'), ('numpy', 'numpy'), ('moviepy', 'moviepy'), ('jsonschema', 'jsonschema')]},
            'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
            'tts': False, 'webgl': False}


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
        for k in spec.get('required', []):
            if k not in value:
                raise ValueError(f'{path}: missing {k}')
        for k, v in value.items():
            if k not in spec.get('properties', {}):
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
    for k, v in [('width', 640), ('height', 360), ('fps', 24), ('seed', 7),
                 ('voice', 'subtitles'), ('webgl', False)]:
        f.setdefault(k, v)
    duration = sum(s['duration'] for s in f['scenes'])
    frames = math.ceil(duration * f['fps'])
    if duration > 120 or frames > 3600 or frames*f['width']*f['height'] > MAX_PIXELS:
        raise ValueError('Film exceeds duration/frame/pixel budget; reduce length, fps or resolution')
    for scene in f['scenes']:
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


def font(size):
    from PIL import ImageFont
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
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

    def render(self, t):
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


def score(f, sample_rate=24000):
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


def encode_frames(f, frames, out, audio):
    ff=capabilities()['ffmpeg']; dur=sum(s['duration'] for s in f['scenes'])
    if ff:
        target=out/'film.mp4'
        with tempfile.TemporaryFile() as err:
            proc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{f["width"]}x{f["height"]}',
                 '-r',str(f['fps']),'-i','pipe:0','-i',str(audio),'-t',str(dur),'-c:v','libx264','-threads','2',
                 '-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-af','loudnorm=I=-14:TP=-1.2:LRA=11',
                 '-ar','48000','-movflags','+faststart',str(target)],stdin=subprocess.PIPE,stderr=err)
            try:
                for im in frames:proc.stdin.write(im.convert('RGB').tobytes())
                proc.stdin.close()
                if proc.wait(timeout=60):
                    err.seek(0);raise RuntimeError(err.read().decode()[-2000:])
            except BaseException:
                proc.kill();proc.wait();target.unlink(missing_ok=True);raise
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
    if f['voice']=='tts':warnings.append('Offline TTS unavailable: rendered subtitles instead')
    if f['webgl']:warnings.append('Offline WebGL unavailable: rendered 2D instead')
    audio=score(f)
    if voice_path:
        v=read_voice(voice_path,dur,out,caps['ffmpeg']);n=min(len(audio),len(v))
        audio[:n]=audio[:n]*.25+v[:n]*.8
    write_wav(out/'mix.wav',audio)
    subtitle_files(f,out)
    frames=(frame_at(f,i/f['fps']) for i in range(math.ceil(dur*f['fps'])))
    try:
        mp4=encode_frames(f,frames,out,out/'mix.wav')
    except (RuntimeError, OSError, ImportError, subprocess.SubprocessError) as error:
        warnings.append(f'Encoder failed ({type(error).__name__}): exported frames instead')
        (out/'film.mp4').unlink(missing_ok=True)
        folder=out/'frames';folder.mkdir(exist_ok=True)
        for i in range(math.ceil(dur*f['fps'])):frame_at(f,i/f['fps']).save(folder/f'{i:06}.png')
        mp4=None
    if not mp4:warnings.append('No MP4 encoder: exported PNG sequence, WAV and SRT')
    sheet=Image.new('RGB',(f['width']*3,f['height']))
    for i,t in enumerate([.1,dur*.5,max(0,dur-.1)]):sheet.paste(frame_at(f,t),(i*f['width'],0))
    sheet.save(out/'contact-sheet.jpg');frame_at(f,dur*.5).save(out/'poster.png')
    (out/'film.json').write_text(json.dumps(f,indent=2))
    (out/'CREDITS.txt').write_text('Style interpretation adapted from Lemomo/LemoLab: https://github.com/lemomo-ai/lemo-opuscar\nMIT code/docs; CC BY 4.0 style adaptations. New procedural graphics and original synthesized score.\nSystem font: DejaVu or Liberation when available (their own licenses). No demo media used.\n'+('Voice: user-uploaded recording.\n' if voice_path else 'Voice: none (subtitles).\n'))
    result={'mp4':str(mp4) if mp4 else None,'duration':dur,'warnings':warnings,'capabilities':caps}
    (out/'result.json').write_text(json.dumps(result,indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('script',nargs='?');p.add_argument('--out',default='artifacts/offline');p.add_argument('--voice');p.add_argument('--capabilities',action='store_true')
    a=p.parse_args()
    if a.capabilities:print(json.dumps(capabilities(),indent=2))
    elif a.script:print(json.dumps(render_film(json.loads(Path(a.script).read_text()),a.out,a.voice),indent=2))
    else:p.error('Provide a script or --capabilities')
