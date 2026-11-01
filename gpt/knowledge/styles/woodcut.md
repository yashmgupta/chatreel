# woodcut

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/woodcut/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Renderer-supported compact port.

Essence, and what it is not:
1. 1. **Black is the wood, white is what the knife removed.** Light is *carved*: a bright area is many wide cuts, a dark area untouched
2. 2. **Pictures appear by being carved.** Nothing fades in: cuts grow stroke by stroke along the form, coarse gouges first, fine lines

Materials & rendering:
1. **Print frame**: the printed image area sits inside a paper margin; the wider bottom margin holds captions. The image edge is the block edge: ragged ink, never a clean
2. **Knife classes** (widths in 1080p pixels at 1×

Colour logic:
1. **At most one colour plate**, printed only where white has been carved, so it glows out of the cuts and never sits on the black. A colour plate over ink is nearly invisible, so plan it on carved

Type & subtitles:
1. **Captions are letterpress in the paper margin**, below the plate, like a plate caption in a woodcut novel. They never cover the image. A letterpress old-style face (IM Fell English, OFL) around 40–44 px, in ink, pushed through the same print shader. The ink…
2. **Titles are carved, not typed**: cut into the block (IM Fell English SC), mirrored if the block is shown before the print is

Motion quality:
1. **Characters on twos (12 fps)**; camera, particles, fire and light on ones (24 fps). Hatching lives in each body part's local space, so cuts move with the limb and don't boil; only fire and liquids re-cut every 2 frames, as deliberate
2. **Anticipation / action / follow-through** on every key action: a few frames back → a 2-frame strike → settle + a short

Sound palette:
1. **Instruments**: low strings (contrabass, cellos; spiccato, pizzicato), wood and skin (log drum, woodblock, frame drum), gran cassa, timpani, one tam-tam, synthesised struck metal (modal: 3–5 inharmonic partials + hammer transient); a bowed saw or hurdy-gurdy…
2. **Options**: withhold the timbre of the story's object until it appears; a metric modulation instead of a tempo jump; a modal shift inside a long decay; one drone under a locked

Native moves:
1. **Light is carved.** A burst of radial cuts from a point. *Fits content like:* a power grid switched on; a scientific insight; a lighthouse
2. **Carving = time.** Patient work on screen, cut by cut. *Fits content like:* a year of training; a building rising; a craft

Pitfalls of the medium:
1. **White marks on white areas are invisible** → stab cuts need dark masses behind
2. **Hatching every surface looks like fur or rain** → grazing light; 3–6 cuts on the lit edge

