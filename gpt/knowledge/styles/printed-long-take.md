# printed-long-take

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/printed-long-take/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **Only ink, paper and one red.** Every value is either ink or paper; grey exists only as a density of lines. One red is reserved for one small subject. A warm yellow may appear for the sun, a lamp or one material, never as a second
2. **Tone is cut, not shaded.** Shadow sides of hills carry knife lines that run down the fall line; skies are parallel horizontal cuts whose width makes the light; snow is paper with a few drift strokes; water is ink with cut

Materials & rendering:
1. **Render model:** three.js scene at 2× supersampling, box-filtered down in a final print pass. Every material is a small shader that decides "ink or paper" per pixel; there is no lighting except one direction used to choose lit and shadow
2. **Two kinds of field.** Every surface is either a paper field carrying ink cuts (lit faces, snow, sand, cloud, foam, steam) or an ink field carrying paper cuts (shadow faces, sky, water, forest, night). A cloud is paper with a few horizontal ink cuts on its…

Colour logic:
1. **One red, reserved for one subject**, kept small (a crown, a lamp, a flag) and never smaller than about 3 px at 1080p; enlarge it a little rather than lose it. It may carry into the subject's own trace (its ripple, its trail), never onto another object. A…

Type & subtitles:
1. **Type lives in the world:** carved into a board, cast on a plate, printed on a pasted notice, or cut as a plate of type into the sky. Words in the world carry only keywords and numbers; no centred title cards, no
2. **Speech and picture move together.** Each line is spoken while the shot shows what it names; the long take keeps going under the voice, and the silent stretches (a hold to read, a pass through a structure, a flock taking off) are left without

Motion quality:
1. **Output 30 fps** (the implementation for the implementation and the implementation). The camera and the world move on every output frame. Separately, the print pass steps its paper flicker and blotches at 12 Hz inside the shader (the implementation),…

Native moves:
1. **The sky carved open.** The sky is cut from the horizon up, one row at a time, the newest row still running across; dawn as a carving, not a gradient. *Fits content like:* a factory's first shift; the first day after a war; a city's lights coming on in…
2. **One red waking.** In a field of ink and paper, the single red appears point by point (heads lifting, windows lighting, flags raised) across the frame. *Fits content like:* poppies opening on a hillside; lanterns along a river; the first lit windows of a…

Pitfalls of the medium:
1. **Close-ups expose the flat shading.** 3D props pushed close to the lens look like toys. Keep living subjects to mid shot as flat silhouettes; give close props real materials (carved wood, concrete formwork, cast
2. **Empty paper.** A field of snow without layers goes blank. Keep three layers in frame; add drift strokes, reed ticks, thickets,

