# game-show

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/game-show/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **Everything is on the grid.** One fixed, fast tempo. Every pop, drop, stamp, typed character and camera punch sits at a (bar, beat) and is also a sound event; the score is generated from the picture's own timeline, so they can't
2. **One drawing kit, many sets.** Flat fills, one heavy ink outline, round caps, hard offset shadows; each round gets a new saturated background colour and

Materials & rendering:
1. **Vector only**, SVG or canvas paths at 1920×1080: flat fills, one outline colour (near-black), 8 px outlines on characters and props, 5–7 px on small parts, round joins and
2. **No gradients, no blur, no texture, no soft shadow.** Depth is a **hard offset shadow**: the same shape in outline colour shifted ~10 px (stickers, banners) to ~14 px (cards), then the coloured shape on

Colour logic:
1. **Ink + paper + candy.** Near-black ink, white, and a warm cream for cards and paper props; around eight saturated candy hues (yellow, orange, red, pink, green, lime, sky, blue) plus two or three deep hues with darker partners for night or finale
2. **One set = one hue.** The background, its pattern and the round card share a hue; the card changes colour to match the set it introduces. Neighbouring rounds never share a

Type & subtitles:
1. **Display**: a heavy rounded sans for Latin and numbers (e.g. Fredoka 700); a black-weight sans for CJK (e.g. Noto Sans SC 900); a hand-lettered face only for handwritten props (e.g. ZCOOL
2. **Telop text**: white or yellow fill with an ink stroke ≈ 14 % of the font size painted *under* the fill (the implementation). Titles are built glyph by glyph so each character can pop

Motion quality:
1. **Idle = hop on the beat**: a parabola per beat (8–30 px); neighbours hop on the off-beat so a crowd
2. **Hit = squash**: a damped wobble (~30 rad/s, ~0.35 s) after each hit; a small squash on every

Sound palette:
1. **All synthesized** from the picture's events: a sine kick with soft saturation, band-passed noise snare and clap, hats, slap bass, detuned-saw brass stabs with a closing filter, square lead with vibrato, marimba-like pluck, music-box bell, triangle pad,…
2. **A bright major pop harmony** on a short chord loop, one chord per bar; each round gets its own flavour (funk, quiz, electro, dream, heavy…), not a new

Native moves:
1. **Rounds with a card.** A 1-bar card (round number + name + a tag such as a year or a step) flies in on a jingle, then play. *Fits content like:* the steps of a recipe; the stages of a startup; the chapters of a museum
2. **Report card.** A typewritten recap with a grade stamp. *Fits content like:* a quarterly review; a trip summary; a final

Pitfalls of the medium:
1. **Stateful updates break parallel renders**: a worker starting cold shows the initial state. Recompute every pose from the implementation; compare single stills with a sequential
2. **Cue lists drift** when cut flashes, jingles and arrangement are separate hand lists: derive them from one

