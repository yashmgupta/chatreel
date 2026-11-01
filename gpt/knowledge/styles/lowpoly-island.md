# lowpoly-island

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/lowpoly-island/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Geometry** (world unit = one hex tile's circumradius): pointy-top hexagonal columns (the implementation), axial → world the implementation, the implementation. Terrain height encodes material (sand low, grass, hills, rock highest). A thin separate top cap…
2. **Props** are primitive assemblies: boxes, prisms, low-segment cylinders and cones, icosahedra at detail 0, pinched boxes. Emissive parts (windows, lamps) get their own material per object so they can light

Colour logic:
1. **Pastel, low contrast, a handful of hues**: one ground family (sand/grass/earth or its equivalent), one neutral rock, and a small set of wall and roof colours repeated across
2. **Time of day is a keyframed set of colours** (zenith, horizon, deep, shallow, sun colour, intensity, elevation, azimuth), interpolated. Day is airy and cool; dusk warms the horizon; night desaturates everything toward

Type & subtitles:
1. **Subtitles**: no box; warm white with a soft dark-blue drop shadow, centred low; a small flat-shaded tile icon beside them whose top colour follows the time of day. Hold ≥ max(1.8 s, speech + 0.6 s), never overlapping the next line or a
2. **Titles behave like tiles**: letters rise one by one from under a water line, overshoot and

Motion quality:
1. **Rise from below**: a short cubic ease up, then a damped-sine overshoot; a splash ring and spray the moment it breaks the surface. The event time is when it
2. **Drop and stack** (floors, roofs, rings): a fast ease-in fall, a damped bounce, and volume-preserving squash-and-stretch on

Sound palette:
1. **Music can be event-driven**: growth events carry a note, and the score synthesizes each one at its exact time, so the picture writes the tune. Pitched percussion suits the facets: marimba, kalimba, woodblock, bells, vibraphone, celesta, steel drum;…
2. **A single note can be a motif**: one sound owned by the world (a bell, a chime, a horn) that returns

Native moves:
1. **Building is composing**: every piece that lands plays a note; a later sweep can replay them in spatial order as a finished melody. *Fits content like:* a skyline whose floors are notes; a team assembling a product; a garden whose flowers form a
2. **Procedural growth**: tiles rise, floors stack, trees pop. *Fits content like:* a startup's first year; a coral reef recovering; a neighbourhood being

