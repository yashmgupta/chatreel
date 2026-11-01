# blueprint

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/blueprint/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Renderer-supported compact port.

Essence, and what it is not:
1. **The whole film happens on one sheet of blueprint paper** lying on a dark drafting table. The camera moves over it like an eye reading a
2. **White line work on uneven Prussian blue**: centre lines, outlines, hatching, dimension lines, leader lines with numbered balloons, a title block, a notes

Materials & rendering:
1. **Sheet**: procedural cyanotype in a shader in *sheet coordinates*, crisp at any zoom: fbm between two Prussian blues, coating streaks, fibres, fold creases (bright edge, dark edge, whitening), bleached edges, specks. Around it: dark drafting cloth with a…
2. **Lines**: pale blue-white, slightly soft (mipmap bleed), a faint ink breakup driven by paper grain. Four weights (outline, detail, thin, hair; e.g. 3.2 / 2.0 / 1.25 / 0.9 sheet units). **Screen width = sheet width × zoom^0.65**, so close-ups don't turn into…

Colour logic:
1. **Blue and white only.** The blue varies in value (coating, stains, folds); the white varies in weight and softness, never in
2. **One non-blue colour, used exactly once**: a rubber-stamp ink (red is classic; a green APPROVED or black VOID work too). It carries the

Type & subtitles:
1. **Hand lettering** for header, labels, notes and subtitles (e.g. Architects Daughter); a technical sans for title-block fields (e.g. B612); a script only for the signature (e.g. Allura). All
2. **Text is written on left to right** with a glowing nib, like everything

Motion quality:
1. **Camera and draw-on on ones (24 fps).** Continuous moves within a section, hard cuts on downbeats between sections; tiny camera bumps only for physical impacts (paper slap,
2. **Draw-on** truncated by arc length with a glowing nib at the head; items staggered within a layer; each layer starts on a

Sound palette:
1. **Contrapuntal, mechanical music**: harpsichord, bassoon, strings spiccato, harp, celesta, music box, clavichord, a small wind ensemble. Imitative lines (an invention, a canon, a fugato) feel like interlocking parts; a short repeated motive can be the
2. **Foley follows materials**. Paper: roll crackle and slap, T-square wood slide, technical pen scratch (2–6 kHz grain, length = stroke length), lettering bursts, compass squeak, hatching strokes, eraser rub, tracing-paper rustle. Brass and wood: part clicks…

Native moves:
1. **Drafting order.** The object draws itself as an engineer would, a layer per beat. *Fits content like:* a bridge; a violin; a kitchen
2. **Live annotations.** Dimensions measure moving parts and the numbers change; balloons fly with parts; a section line reveals the inside. *Fits content like:* a heart valve; a folding bicycle; a rocket stage

Pitfalls of the medium:
1. **Main figure near the sheet edge** → wides show the desk. Keep margins or enlarge the
2. **Upward explosions hit the header** → explode sideways and flatten long parts during the

