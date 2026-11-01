# halftone-dossier

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/halftone-dossier/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The whole film is paper.** A warm cream sheet with low-frequency mottling, fine grain, a vignette and a fold; dark scenes are printed on it too, never
2. **Shading is never a gradient**: it is halftone dots whose size follows a density field. Two or three dot layers at different screen angles overprint (multiply); that is the "printed"

Materials & rendering:
1. **Paper layer** (canvas, multiply over everything, built once): an upscaled random tile for mottling, per-pixel noise with a slight warm bias, a radial vignette, a faint centre
2. **Grain layer** (per frame): a few hundred paper-coloured specks and fewer ink specks, reseeded every 2 frames: dust on the print, not film

Colour logic:
1. **A paper ground, one dark ink, and four or five flat spot inks.** The dark ink (navy, black-brown or deep green) carries every outline, body text and the caption bar, and is the fade-out
2. **Night or "secret" scenes** switch to a dark ink ground with a lighter dot layer of the same family, still multiplied by the

Type & subtitles:
1. **Headlines**: a black-weight serif (e.g. Noto Serif SC 900 for CJK; a black slab for Latin), 100–230 px, left-aligned near the margin, with a **misregistration shadow** (+8/+8 px in the overprint ink,
2. **Display / numerals**: a fat rounded display face (e.g. Bagel Fat One) for names, big numbers,

Motion quality:
1. **Everything enters with overshoot** (back ease, 0.3–0.45 s): rising from below the frame or scaling from 0. Nothing fades
2. **Per-character pop** for headlines: each glyph drops 30–100 px and squashes in, stagger 0.05–0.08 s (0.02 s for small

Sound palette:
1. **Synth pop-print toolkit**: synth kick, snare, clap, hat; a square-ish 8th-note bass; triangle pad; a **marimba-like pluck** (fundamental + ~4× partial) for melody; pizzicato and finger snaps for sneaking; music-box bell for
2. **Foley follows the print and the gag**: stamp = pitch-dropping boom + click (a crackle for big ones), camera shutter, paper slides and folder flaps, typewriter or keyboard clicks, whooshes into wipes, pops on every glyph, boings and plops for characters,…

Native moves:
1. **The accusation frame.** A topic becomes "the case of X": list its counts. *Fits content like:* a cognitive bias on trial; a city's traffic problem; a plant that won't stop
2. **Numbered exhibits.** Each beat gets a giant halftone numeral behind it. *Fits content like:* five causes of a blackout; three clauses of a contract; the stages of a

Pitfalls of the medium:
1. **Fonts not loaded before layout** → per-character positions computed with a fallback font, glyphs overlap. Preload every family against the whole page source and the built text; runtime strings must use only characters that appear in the file. Use the…
2. **Boil on text or dots** turns them to mush → filter only characters and

