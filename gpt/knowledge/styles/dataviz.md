# dataviz

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/dataviz/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Paper**: warm cream, fixed-seed fibre noise and a faint dot grid in world space. **Ink**: dark warm ink for axes and series, pale warm grey for grid and zero line, IBM Plex Mono
2. **Marks**: data dots carry a thin ink ring so pale values stay visible on cream. A mark lands with a short pop and a thin ripple; suppress ripples when marks arrive closer than ~0.1

Colour logic:
1. **Honesty beats drama**: pale values stay pale; never stretch a ramp to make a change look

Type & subtitles:
1. **The subtitle is the figure caption**: a text serif (Newsreader), ink colour, left-aligned with the chart, ≤ 2 lines, with a hairline rule above it and a small mono kicker for the range drawn so far. Words appear on their whisper timestamps over a…

Motion quality:
1. **The rhythm of the data is the rhythm of the film.** Map the marks to a musical grid; to accelerate, one option is to **divide the beat instead of changing tempo**. Pick a tempo whose finest subdivision lands on whole frames (at 24 fps a minute has 1440…
2. **Pencil acting**: lift before each tap, land with the shadow meeting the tip, a tiny rebound; hurry as data densifies, tremble like a seismograph needle at a peak. It can **flinch** (recoil and freeze), **hesitate** (hover before a mark) and **exit** (hand…

Sound palette:
1. **Ambience** follows the places the notes evoke (J-cuts in, L-cuts out). **Foley** is graphite, paper and wood: tick-and-paper taps, scratches for handwriting, a ruler hiss for axes, a paper puncture for a broken frame, a wooden click for the pencil flip,…
2. **Sonification** is the music: pitch = value, rhythm = time density. Low values snap to a pentatonic scale, middle ones to semitones, extreme ones unquantized, with detune growing away from the reference. Timbre: a **low-pass-gate "plonk"** (sine + FM whose…

Native moves:
1. **One mark = one fact.** *Fits content like:* the first store a chain opened; the first patient of a trial; the first satellite
2. **Axes grow with the story.** The y axis arrives when the narration first names the unit. *Fits content like:* revenue; a city's population; vaccination

