# hd-2d

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/hd-2d/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Constant texel density**: surfaces drawn per pixel on small canvases, the implementation, world-space UVs at one density (e.g. 24 px/m); sprites on a similar scale (a character ~30–60 px
2. **Colour from ramps**: 3–6 swatches picked by brightness through a narrow 4×4 Bayer dither. Sprites get a 1 px *selout* outline (neighbour colour darkened toward the

Colour logic:
1. **Two temperatures**: one large ambient key (cold, or pale, or dusty) against small warm or saturated practicals. The practicals carry the story; the ambient carries the

Type & subtitles:
1. **Narration subtitles**: italic serif ~46–54 px, centred low on a soft dark gradient band, one line per voice clip, in ~0.35 s before the
2. **On-screen speech gets a dialogue box**, not a subtitle: dark plate, thin metal border, corner ornaments, name plate on its top edge, text **typed over ~90 % of the voice**, blinking caret, soft chime on

Motion quality:
1. **Sprites step, everything else glides.** Walk cycles 4 frames at 6–10 fps, idles alternate two frames at ~1–2 Hz, blinks every few seconds, pose changes are instant cuts between drawings. Camera, lights, particles, beams and focus update every output frame…
2. **Poses are data**: a parameter object per drawing; a new pose is a new table

Sound palette:
1. **Music**: chamber-fantasy or cinematic colours (harp, celesta, strings, horns, low choir, timpani) or small folk instruments (lute, recorder, hand drum). Either one piece whose own arc matches the story, **cut inside it** at downbeats, or an original score;…
2. **Silence as a tool**: a hard stop into a reverb tail, a pad alone, or one heartbeat when the light nearly dies; a short breath (< 1 s) when something

Native moves:
1. **Shadows jump when a light is lit.** A practical turns on next to sprites and their shadows swing across the floor. *Fits content like:* a shop opening at dawn; a server rack powering up; a teacher switching on a
2. **The carried light as a meter.** One small light a character carries is key light and gauge at once: its brightness rises and falls with whatever the story is measuring. *Fits content like:* a phone battery on a long trip; a patient's heart monitor; a candle…

Pitfalls of the medium:
1. **Checkerboard everywhere** → the dither band is too wide (≈ .22 on sprites, ≈ .45 on
2. **A light burns out the sprite that holds it** → move the light ~0.45 m toward the camera; cap sprite lighting in the shader (the

