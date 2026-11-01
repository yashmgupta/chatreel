# satellite-briefing

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/satellite-briefing/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The ground is a photograph**: real, licence-clean, georeferenced satellite or aerial imagery of the actual place. Nothing on the ground is drawn, stylised or
2. **Two layers, two truths**: the imagery is what the satellite saw; the hairlines are what the analyst measured. Marks are thin, white, sparse, and sit on real

Materials & rendering:
1. **Plates**: georeferenced rasters with a lon/lat box, sampled in a shader where the camera ray hits the ground, nested by resolution (world → region → detail) with feathered edges so finer plates dissolve in as the camera
2. **Globe**: ray–sphere from a perspective camera, a thin atmosphere rim, limb shading at orbit only; compute |C|² − R² in double precision (float32 fails below a few tens of

Type & subtitles:
1. **Roles**: a light condensed grotesk for the reading (96–130 px, e.g. Barlow Condensed); a monospace for instruments and dates (20–34 px, e.g. IBM Plex Mono); a sans for labels in the film's language (24–42 px); a serif only for the claim layer and the title.…
2. **Labels attach to the ground** with a leader line. The reading sits in the right third beside what it measures, label above, source note below ("Landsat,

Sound palette:
1. **Telemetry**: FM pings (a lock-on ping worth bringing back), dry ticks on the grid that divide to accelerate, noise scans (rising for a rewind, falling forward), servo whines, a ratchet for a range
2. **Weight**: timpani, bass drum, gran cassa, bowed cymbal, a tam-tam reversed when time runs backwards. Measurements land on a pitched

Native moves:
1. **The map against the photograph.** The camera falls into the printed map of the claim; a scanner bar tears it away and the ground is underneath; the name outlives the page. *Fits content like:* a lake still on maps but gone; a cleared concession forest; a…
2. **Time rings in a locked frame.** Dated plates scan in one by one; each leaves its outline, the band lost between two rings flashes. *Fits content like:* a glacier's retreat; a city's sprawl; a fire scar season after

Pitfalls of the medium:
1. **Licences**: not usable: Google Earth/Maps, Bing, Esri World Imagery, Mapbox Satellite, Planet, Maxar, news photos, AI-generated imagery. EOX Sentinel-2 cloudless is CC BY 4.0 only for 2016 (2018 onward is NC). Raw Copernicus Sentinel data need "Contains…
2. **Finding imagery for a new place**: search by bounding box and date in the Planetary Computer STAC (Landsat C2, Sentinel-2 L2A; no account) or USGS EarthExplorer; MODIS/VIIRS and Blue Marble from NASA GIBS; coastlines, lakes and rivers from Natural Earth…

