# ascii-crt

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/ascii-crt/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Font**: one monospace bitmap-style font (VT323, OFL); cell 0.4 em × 0.8 em (1:2). A large prerendered glyph atlas with a stroke for beam spread, scaled with the implementation, keeps zooms continuous and
2. **Grids**: column count per shot (title ~20, terminal 80, picture 200+); a push-in can go until one cell holds a sub-grid of its

Colour logic:
1. **One phosphor** carries everything: amber, green or white, in its own brightness ramp. No second hue for
2. **At most one soft second colour**, used for one thing only (the emotional object), switched on at a single moment, on a downbeat, and never taken back

Type & subtitles:
1. **Subtitles are terminal output.** A reserved **LOG strip** at the bottom: a dim separator, an inverse-video tag, then a prompt and the line in uppercase at ~45 px. It is **typed word by word in sync with the voice** (whisper word timestamps) and holds ≥…
2. **On-screen text that the story shows** is picture, not subtitle; in the the implementation it appears as the

Motion quality:
1. **Characters never move off-grid, except in a declared transformation moment.** Typing, scrolling and counters jump from cell to cell. A roller flips digits discretely, fast then
2. **Only three things move continuously**: grid scale (the camera), CRT physics, and particles in a

Sound palette:
1. **Music**: an original analog-synth score, rendered in code (numpy / numba): PolyBLEP saw and square oscillators, a resonant 4-pole ladder filter with moving cutoff, filter envelopes, square-wave sequencers, slow tape wow (± a few cents), long reverb on pads,…
2. **Technique options**: grow a single arpeggio as an image forms; hold the only major chord for one moment; drop everything, reverb tails included, to digital zero on a shock; open a chord on the colour

Native moves:
1. **The picture is made of words.** A sentence breaks apart and its letters, sorted by ink density, become an image containing only those letters. *Fits content like:* a manifesto becoming a crowd; a recipe becoming the dish; a poem becoming a
2. **Font size = camera.** Push until one character fills the screen and is itself made of smaller text. *Fits content like:* a company name made of employee names; a year made of its headlines; a heart glyph made of

Pitfalls of the medium:
1. **Inverse video**: the implementation only changes alpha, which the upload ignores → opaque black canvas, cut letters with a *black*
2. **Negative not aligned to the grid** drifts across hundreds of columns → map with cell width / samples

