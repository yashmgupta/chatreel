"""Conventional synthesis only: no models, samples or network."""
import math
import numpy as np


def arranged_score(film, rate=24000):
    duration=sum(s['duration'] for s in film['scenes']);n=round(duration*rate)
    mix=np.zeros(n,dtype=np.float64);cfg=film.get('music',{})
    if not cfg.get('enabled',True):return mix
    gain=cfg.get('gain',.15);beat=60/cfg.get('bpm',96);rng=np.random.default_rng(film.get('seed',7))
    def add(at,hz,length,level,voice):
        start=round(at*rate);size=min(n-start,round(length*rate))
        if size<=0:return
        t=np.arange(size)/rate
        if voice=='pluck':
            wave=np.sin(2*np.pi*hz*t)+.22*np.sin(2*np.pi*hz*2*t)*np.exp(-t*6)
            env=np.minimum(t/.008,1)*np.exp(-t*4)*np.minimum((length-t)/.06,1)
        elif voice=='pad':
            wave=(np.sin(2*np.pi*hz*t)+.12*np.sin(2*np.pi*hz*2*t))/1.12
            env=np.minimum(t/.22,1)*np.minimum(np.maximum(length-t,0)/.35,1)
        else:
            wave=rng.normal(0,1,size);wave=np.diff(wave,prepend=0)*.25
            env=np.exp(-t*35)*np.minimum(t/.002,1)
        mix[start:start+size]+=wave*env*level*gain
    # Quiet chord bed and syncopated mallet-like motif; space is left for captions/voice.
    chords=[(48,55,60,64),(45,52,57,60),(53,60,65,69),(43,50,55,59)]
    for bar,at in enumerate(np.arange(0,duration,beat*4)):
        chord=chords[bar%4]
        for note in chord[1:]:add(float(at),440*2**((note-69)/12),min(beat*4,duration-at),.13,'pad')
        for k in (0,1.5,2.5):
            note=chord[(bar+int(k))%len(chord)]+12
            add(float(at+k*beat),440*2**((note-69)/12),.65,.55,'pluck')
        add(float(at+beat),0,.15,.12,'brush')
    start=0
    for scene in film['scenes']:
        add(start,880,.10,.14,'pluck');start+=scene['duration']
    for cue in cfg.get('cues',[]):add(cue['time'],440*2**((cue['note']-69)/12),cue.get('duration',.4),.6,'pluck')
    # Smooth entrance/exit, no discontinuity at the last sample.
    ramp=min(round(.18*rate),n//2)
    if ramp:mix[:ramp]*=np.linspace(0,1,ramp);mix[-ramp:]*=np.linspace(1,0,ramp)
    peak=float(np.max(np.abs(mix))) if n else 0
    if peak>.8:mix*=.8/peak
    return mix


def mix_voice(music,voice,offset=0,rate=24000):
    """Windowed energy ducking with a short attack and slower release."""
    count=min(len(voice),len(music)-offset)
    if count<=0:return music
    voice=voice[:count]
    envelope=np.empty(count);hop=max(1,round(rate*.01));gain=1.
    for start in range(0,count,hop):
        end=min(count,start+hop);rms=math.sqrt(float(np.mean(voice[start:end]**2)))
        target=.22 if rms>.012 else 1.
        smoothing=.65 if target<gain else .07
        next_gain=gain+(target-gain)*smoothing
        envelope[start:end]=np.linspace(gain,next_gain,end-start);gain=next_gain
    result=music.copy();result[offset:offset+count]=result[offset:offset+count]*envelope+voice*.82
    peak=float(np.max(np.abs(result)))
    return result*(.96/peak) if peak>.96 else result
