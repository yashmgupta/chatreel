# ink-wash

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/ink-wash/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Paper** is procedural, in the compositor, never a texture file: warm rice paper (around the implementation), cloud mottling, long fibres, pulp flecks, grain that fades when zoomed out (or it shimmers), a light vignette; anchored to the
2. **Ink** is stroke opacity multiplied onto paper (never an overlay), in five tones

Colour logic:
1. **One vermilion** (around the implementation), for the seal and at most one tiny accent in the story (an object the protagonist carries). The accent finds the protagonist in wide shots and can rhyme with the seal. Never a red wash, never red

Motion quality:
1. **Figures step at 12 fps** (on twos); their position, the camera, blooms, ripples and splatter move on ones at 24
2. **Stable strokes on twos**: seed every stroke by its index and compute bristle breaks along *normalized* arc length × a fixed reference length, so flying-white gaps don't crawl every drawing. Allow only a small "boil" on the width

Sound palette:
1. **Guqin-led, not piano and strings**: guqin (the implementation the implementation: open and stopped strings, slides, vibrato, glassy harmonics, sweeps), a low breathy xiao, big drum and timpani for mass, frame drum for steps, a small gong for a seal. Chinese…
2. **Cue to the picture, never loop**: unmetred plucks suit emptiness, a pulse suits movement, rolls suit mass; painted strokes can each land on a

Native moves:
1. **One stroke is everything.** *Fits content like:* a product born from one line; a city growing from a single street; a day beginning with one
2. **Emptiness is matter.** Removing ink reveals paper white. *Fits content like:* a door opening in a wall; a crowd parting; an absence in a family

