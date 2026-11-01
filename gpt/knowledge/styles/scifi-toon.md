# scifi-toon

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/scifi-toon/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Line**: near-black (a slightly purple black reads best), ~7 px for characters and props, 4–6 px for background detail, round joins. **Line width is constant in screen space**: close-ups are "redrawn" at the same weight, never scaled up (transform points to…
2. **Line boil**: resample every outline in screen space (~7 px steps) and displace along the normal with low-frequency noise, amplitude ~1.7 px; cycle **3 boil drawings at 12 fps**. Everything boils, including held poses and backgrounds: a still frame is never…

Colour logic:
1. **One palette per world**, 3–5 colours, maximally different from the previous world in hue *and* value, so the audience reads "we jumped" from colour

Type & subtitles:
1. **Subtitles**: bottom centre, a rounded heavy sans (Baloo 2 ExtraBold ~50 px), white with a ~11 px black outline, so they look like the cartoon's own captions, with a small **speaker pill** in the character's colour (boiling outline) on the left. Lines over…
2. **Timing**: hold ≥ max(1.8 s, speech + 0.6 s) for narration; for rapid dialogue, the implementation. Clip at world changes and **before a silent beat**, so the silence plays on a clean

Motion quality:
1. **Characters on twos (12 fps)**: poses, mouths, blinks, walk cycles and boil step at 12 fps. **Camera moves, portal swirl, flying props and wipes on ones (24
2. **Acting over moving**: held poses with small changes (eye twitch, pupils sliding, a gulp, sweat drops). Idle life: breathing (±1 % squash), a nod driven by speech

Sound palette:
1. **Synthesized score, no samples needed.** A **theremin**-like lead (sine + a little 2nd/3rd harmonic, legato portamento ~70 ms, vibrato fading in ~150 ms after each onset, spring reverb) over analog bass, a square-wave arpeggio and a retro drum machine. Minor…
2. **Genre cues per world** (options): surf guitar; polka accordion; toy-piano lullaby; elevator bossa (Karplus–Strong nylon guitar); brushed swing with vibes; tuba + slide whistle; warm Rhodes + a vocal "aah"; tremolo strings for

Native moves:
1. **Parallel worlds.** Each jump = new palette, new cue, new creature. *Fits content like:* versions of a product; careers you could have had; the same city in five
2. **Duo contrast.** Deadpan vs panic: the joke is in the difference between reactions. *Fits content like:* a veteran and a new hire; a parent and a teenager; an AI and its

