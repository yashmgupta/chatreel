# lidar-survey

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/lidar-survey/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The cloud is the data**: every point is a real return at its measured position; points appear, glow, lift away or give way to a surface, but are never moved into a
2. **Points become a surface**: a front (scan line, cutting plane) behind which the cloud condenses into a solid model of the same

Materials & rendering:
1. **Points**: GL points sized in world units (0.12–0.3 m), floor of one output pixel, soft discs, opaque and depth-tested (additive only for a ghost layer); colour from height or class, value from intensity; distance
2. **Quantise for the browser**: uint16 positions (2 cm / 1 cm) plus a byte each for height above ground, class, intensity,

Type & subtitles:
1. **Roles**: light condensed numerals for readings (110–130 px, e.g. Barlow Condensed 300); a monospace for instruments, coordinates, counts and source lines (19–22 px, e.g. IBM Plex Mono); a sans for labels in the film's language (24–36 px, e.g. Noto Sans SC…
2. **Instruments** in one corner: place, coordinates, area, data source, point count, any exaggeration; they change only when the medium

Sound palette:
1. **Instrument sounds**: FM pings, fine crackle as points arrive, noise sweeps tied to a front, ticks that divide (8ths → 16ths → 32nds) to accelerate, a descending pitched blip per peeled layer, a ratchet while a counter rolls, a ping when a reading
2. **Weight and synthesis**: timpani, bass drum, gran cassa for condensations and cuts, a reversed swell into the main impact; low-passed detuned-saw pads; a pulse bass with audible 2nd/3rd

Native moves:
1. **Photo to points.** A scan line crosses an aerial photo; behind it the place is points. *Fits content like:* a site visit before a design; what the satellite misses; a quarry's real
2. **The canopy peel.** A plane descends by height above ground, returns above it lift away layer by layer, a ruler tracks it. *Fits content like:* archaeology under forest; a hidden trail; flood channels; landslide

Pitfalls of the medium:
1. **Finding data for a new place**: USGS 3DEP (US) as Entwine Point Tiles per project at the implementation, projects and footprints in the implementation of github.com/hobuinc/usgs-lidar; bare-earth scouting through the 3DEP elevation ImageServer.…
2. **Licences**: public domain, CC0, CC BY and attribution-only government licences are fine, with credit in the implementation. ODbL, CC BY-SA, "no known restrictions" (not CC0) or non-commercial terms: name them to the user and ask first. Never commercial…

