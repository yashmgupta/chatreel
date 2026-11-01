# swiss-motion

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/swiss-motion/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Renderer-supported compact port.

Essence, and what it is not:
1. **Pure 2D graphic design animated on a grid**: flat paper, black type and bars, a very light grey and **one** saturated signal
2. **Every element snaps to the grid, every move lands on a beat, nothing

Materials & rendering:
1. **Frame grid**: 1920×1080, 12 columns, ~96 px side margins, 24 px gutters, 24 px baseline. The frame can act as a **spread**: a left page (the programme: numeral, rule text, notes) and a right page (the
2. **Artifact grid** derived from the content (Gerstner): what the columns and rows *mean* is a design decision. **Choose module sizes that give the elements mass**; too many thin columns make a layout look like a

Colour logic:
1. **Paper, ink, greys, and one signal colour.** Only one thing carries the signal colour; that makes it the protagonist. It is the only thing allowed to be

Type & subtitles:
1. **One family for the whole film**, an OFL neo-grotesque (Archivo, Inter, Schibsted Grotesk, Instrument Sans…), several weights. Letter-spacing ~−2 % at ≥ 90 px. Headlines can be lowercase. Load every weight with the implementation before
2. **Flush left, ragged right**; everything on a grid line; big white space is part of the layout. Giant numerals are **optically** flush left (subtract the glyph's left

Motion quality:
1. **Two curves only**: a precise ease the implementation for snaps; linear for lines being drawn, playheads and the exception. No overshoot, no spring, no
2. **Durations are note values** at the film's tempo. A snap starts one note value early and **lands on the

Sound palette:
1. **Music with a grid of its own**: a steady pulse whose subdivisions give snap durations. Options: motorik / krautrock kit and bass, minimal techno, marimba or vibraphone patterns, a mechanical piano ostinato, a drum machine with a glockenspiel; one instrument…
2. **Picture and music can share one data file** (a column → pitch, a row → onset), so a graphic can literally be the

Native moves:
1. **The grid means something.** Columns and rows become a quantity (notes, hours, floors, years). *Fits content like:* a building's floors and rooms; a week's timetable; a city's
2. **Snap = beat.** Every arrival is a percussion hit. *Fits content like:* a product's feature list; the steps of a recipe; a

