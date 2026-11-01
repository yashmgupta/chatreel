# transit-map

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/transit-map/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **Eight directions only.** Every line segment, river edge and coastline is horizontal, vertical or at 45°; every corner is one fillet radius. A line never
2. **Growth is drawing.** A line exists as far as its pen tip has travelled; stops light when the tip passes; an interchange appears only when the second line actually arrives, and it lands with

Materials & rendering:
1. **Interchange shape follows the station.** Points side by side make a horizontal stadium, stacked points a vertical one; lines that cross at one point make a circle r 0.13 with the ink outline, which reads as an interchange next to the 0.085 stop because of…
2. **Two passes.** A 2D canvas inks only the region the camera sees into a texture (about 1.35× the screen density at the focus, capped at 4096², mipmapped, anisotropic filtering), limited in depth to a few camera distances so low views don't starve; a WebGL…

Colour logic:
1. **Line colours carry identity and nothing else.** A real network uses its published colours; an invented one picks hues spaced around the wheel at similar weight, never two neighbours
2. **Mode is carried by line form, never by hue.** Each line keeps its colour whatever kind of vehicle runs on

Type & subtitles:
1. **Faces**: a neutral grotesk for Latin and figures (Inter in the demo) and a CJK sans of matching weight (Noto Sans SC, subset to the characters used). OFL, self-hosted. Native language above, second language below, one line each, never
2. **Sizes on the sheet**, in G (native / second language): hub label 0.30 / 0.17 bold; interchange 0.23 / 0.14 semibold; named stop 0.20 / 0.14 semibold; the second line in warm grey, 0.03 G below. Callout: date figures 0.58 heavy, native line 0.34, second line…

Sound palette:
1. **Tuned percussion** for drawing and stops: glockenspiel, marimba, vibraphone; a stop is a pluck, an interchange a pop with a low
2. **A two-note station chime** as the motif, returning at the turns of the

Native moves:
1. **The pen tip.** A glowing tip draws a line at the camera's pace; stops light behind it. *Fits content like:* a product roadmap; a migration route; a career, job by
2. **The interchange that falls.** When two lines meet for the first time (a second line arriving, or leaving from a station already drawn) the capsule drops onto the paper with its shadow, then shock rings in both colours. *Fits content like:* two teams…

Pitfalls of the medium:
1. **Off-grid geometry**: any segment not at 0/45/90° breaks the style. Route between points with an automatic bend (straight then diagonal, or the reverse) and validate every
2. **Labels over lines, or labels that jump**: give labels a paper halo and place them once against the finished network, before the first frame. Placing against what is drawn so far makes labels hop as lines

