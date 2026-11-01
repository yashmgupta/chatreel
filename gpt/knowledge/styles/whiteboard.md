# whiteboard

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/whiteboard/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **One physical whiteboard.** Everything the viewer learns is drawn in dry-erase marker in front of them, in real handwriting
2. **The board is a map**: each idea lives in its own region; the camera travels between regions, often led by the pen. Distance on the board = distance in the

Materials & rendering:
1. **Board**: a warm white gradient, a faint scuff and micro-scratch tile, a few dozen **ghost marks** (old words, circles, arrows) at 5–10 % in grey or pale blue, and a soft diagonal **window sheen** (white, 10–16 %) moving at ~0.35× the camera: this one detail…
2. **Ink**: alpha ~0.94, composited with **multiply** so overlaps darken like real marker. Width 6–11 px for drawing, ~13 % of cap height for

Colour logic:
1. **Three marker colours at most**, each with a meaning held for the whole film: one dark ink for things and structure, one for signals / measurement / process, one accent for the thing that matters (one accent per
2. **Monochrome variant**: everything in the dark ink, one element in the accent (the "only

Type & subtitles:
1. **Handwriting only**: a single-line hand (e.g. EMS Tech, OFL) for all board text; titles large (~120–200 px cap height), labels 30–70
2. **Title and end card are written on the board** in the same

Motion quality:
1. **Hand speed**: every stroke follows a slow-fast-slow curve (the implementation). Strokes are scheduled into a **time window** and the engine solves the speed, so writing always finishes on
2. **Pen hops** between strokes lift in proportion to distance (shadow slides and blurs); long gaps send the pen off-frame to park and back shortly before its next

Sound palette:
1. **Every stroke sounds**: band-passed felt-on-gloss noise (a hiss band ~2–7.5 kHz + body ~0.5–1.5 kHz) enveloped by the stroke's own speed curve, a tiny nib tick at the start, stick-slip grains, and on some long strokes the **dry-erase squeak** (a 1.5–2.6 kHz…
2. **Props**: magnet on steel = click + metal modes + a low board thump; eraser = felt rub modulated by its zig-zag; cap off/on; marker tray

Native moves:
1. **Writing in stroke order.** The reveal is the explanation: a formula term by term as it is spoken. *Fits content like:* compound interest; the Drake equation; a recipe's
2. **The pen leads the camera.** Transitions are drawn lines the camera rides. *Fits content like:* a nerve signal; a supply chain; the water

Pitfalls of the medium:
1. **One pen, too many jobs** drifts later and later → give each drawing a deadline window and let overlapping jobs go to another
2. **Minimum stroke duration × many dashes** makes a dashed line take seconds → dashes need their own

