# iso-infographic

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/iso-infographic/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **Flat, true isometric.** No perspective, no outlines on solids; shapes are separated only by the three tones of each face. The projection never rotates or
2. **Infographic furniture is part of the picture**: leader lines, label pins, dashed cut lines, hatched section faces, tracking rings, a legend, a route line all live in the

Materials & rendering:
1. **Projection**: axes at 30°. the implementation, the implementation; x runs down-right, y down-left, z up; painter depth = x + y + z. Everything is queued and depth-sorted, then
2. **Three tones per face** chosen from its normal: top light, left (+y) mid, right (+x) dark. Derive tones from one base colour: mix toward warm white ~20 % for the top and toward a cool dark (e.g. the implementation) ~22 % for the dark side, so shadows are…

Colour logic:
1. **A pale neutral ground** (cream, paper grey or pale blue) and **5–7 flat hues**, each with its three tones; one ink
2. **Colour codes meaning**, the way a legend does: one hue per material or role (water is always the same blue, the subject always its hue). Never reuse a hue for two

Type & subtitles:
1. **Label pins**: dot (ink ring, pale fill) → vertical leader → horizontal rule → text. Pins point up or down, left or right, chosen per station so labels never cover the
2. **Titles** can be isometric type on a world plane, extruded as

Motion quality:
1. **Nothing moves without a line leading it**: a route line is drawn slightly ahead, a leader grows before an inset opens, a cut line draws before a skin slides
2. **Cutaway**: cut line (~0.3 s) → the near skin slides out along its normal and fades (~0.35 s, ease-out) → hatched section rims fade in over the last

Sound palette:
1. **Music**: acoustic and light: kalimba, marimba, nylon guitar, pizzicato, woodblock and hand percussion (shaker, bongo, cajon), upright or synth bass, glockenspiel, toy piano, or a clean electronic pulse for technical systems. A short motif can mark the…
2. **Techniques (options)**: one sound per icon as numbers fill; instruments dropping out and a low-pass closing as the camera dives; J-cuts (the next station's sound 0.5 s before it appears); one note per station during a final

Native moves:
1. **Cutaway.** Cut line, skin slides away, hatched rims remain. *Fits content like:* a heart's chambers; a server rack; a
2. **Isotype number.** Identical icons in a new arrangement each time (a calendar, a bar, a silhouette formed by the icons themselves). *Fits content like:* votes in an election; litres of water per product; users of an

