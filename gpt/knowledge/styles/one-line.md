# one-line

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/one-line/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **One continuous line** on warm white paper. The pen never lifts: in code the whole film can literally be one point array, from the first touch of the nib to the last
2. **Everything is a line**: characters, places, objects, even time. No fills, no shading, no second line weight, no background

Materials & rendering:
1. **Paper**: warm white (around the implementation), procedural mottling (soft-light, large tile), long fibres that fade out when zoomed out (or they shimmer), a sparse paper-tooth speckle over the ink at close zoom, light vignette. All textures anchored to the…
2. **Ink** is a filled polygon around the path (not the implementation), mixed with paper colour to an opaque tone per

Colour logic:
1. **Ink on paper.** A warm black (around the implementation) on warm white; nothing else fills the
2. **One accent at most, used once**, on a stretch of the line that means something; it returns to ink afterwards and stays visible in the final picture if the picture is

Type & subtitles:
1. **Text is written, like the line**: a handwriting face (e.g. Caveat) for subtitles, ink at ~84 %, no box, centred near the bottom, **written on** left to right (~0.2 s + ~17 ms per character) behind a soft paper-coloured halo so passing lines never cross the…

Motion quality:
1. **Everything on ones** (24 fps): the appeal is the continuous act of drawing; stepping breaks
2. **Timing = chapter windows + curvature**: within a window, time per point is weighted by the implementation (sharp turns get more time, smoothed so speed never jumps). Pin musical beats with marks: by arc-length fraction or by position ("the second time the…

Sound palette:
1. **Music: one solo instrument, one unbroken melodic line**, the sound equivalent of the drawing: a bowed or plucked string (cello, violin, viola, harp), a solo woodwind (clarinet, flute, bassoon), a hummed voice, a single guitar. A second colour only as a rare…
2. **Write the score to the drawing**: key notes on marks and corners; fast line = short notes; a stopped line = one long note fading into silence; the highest note on the most important

Native moves:
1. **The pen never lifts.** Anything that is one continuous thing. *Fits content like:* a river from source to sea; a relay race; a production
2. **The line is time.** The stroke's character changes with age, mood or strain. *Fits content like:* a building aging; a runner tiring; a machine wearing

Pitfalls of the medium:
1. **Stray connectors ruin a reveal**: every extra line reads as a wrinkle, beard or mask. Fix the topology (where each chapter enters and leaves), not the drawing. Plan it like an Euler path: a closed motif is a circuit (you leave where you came in); retrace or…
2. **Test the reveal early and often**: render the whole path at once at final scale after every

