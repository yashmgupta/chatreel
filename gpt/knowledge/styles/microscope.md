# microscope

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/microscope/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The specimen is a photograph**: a real micrograph or whole-slide scan of the actual sample, CC0, public domain or CC BY. Nothing on the specimen is drawn, retouched or generated. A whole-slide image (WSI) is the ideal source: one sample, one registered…
2. **Scale is the camera**: one log-space dive (and, when the story wants it, the climb back) through nested plates of the same sample. The scale bar shortens and jumps in a 1-2-5 sequence, the field-of-view readout rolls, the magnification

Materials & rendering:
1. **Plates**: the WSI pyramid levels as plates in one world frame (level-0 pixels), the coarse levels whole and alpha-feathered at the scan edge, the fine levels as crops around where the camera lands. Each frame draws the finest plate that is downsampled no…
2. **The naked-eye plate**: the scanner's own photo of the whole slide (many WSI files carry one), registered through the scan's area-of-interest metadata and checked against the tissue's centroid. Cut the glass out of the scanner tray, remove the line-sensor…

Type & subtitles:
1. **Roles**: a light condensed grotesk for readings and the scale bar (40–72 px, e.g. Barlow Condensed); a monospace for instruments and pixel counts (20 px, e.g. IBM Plex Mono); a sans in the film's language for labels (20–34 px, e.g. Noto Sans SC); a serif…
2. **Instruments** live in one frosted panel in a corner: scale bar with its value, field of view, magnification with a small nosepiece glyph that turns a quarter on every change. The source credit in a small panel in the opposite

Sound palette:
1. **Instrument foley**: the objective turret (a click, a detent, a small metal ring), a focus servo, pen on glass for each line drawn, a band-passed scan travelling left to right with counter ticks that speed up, a soft filtered sweep for the focal
2. **Music**: hard-mallet vibraphone in 8ths and 16ths, marimba ticks, bowed vibraphone and water glasses for pads and the motif, glockenspiel for each reading that lands, a pulse bass with 2nd/3rd harmonics, timpani and bass drum under the landings. Harmony…

Native moves:
1. **The dive.** From the slide in the hand to a cell in one camera, the turret clicking at each real change of level. *Fits content like:* a biopsy to its cells; a coated surface to its crystals; a hair or skin section to its
2. **Counting the colour.** Draw a circle, let a scan front cross it, light up every counted pixel and roll the share up to its landing value; show the raw counts underneath. *Fits content like:* collagen in tissue; porosity in a ceramic; coverage of a coating;…

Pitfalls of the medium:
1. **Licences**: most microscopy on the web is CC BY-NC or all rights reserved. Usable: CC0 whole-slide scans (e.g. the OpenSlide test data: check each file's licence line), public-domain government micrographs (NIH, CDC PHIL, NASA, USGS), CC BY collections…
2. **Finding material for a new topic**: search by organ, stain or material plus "whole slide" in the OpenSlide test data, NCI Imaging Data Commons (TCGA/CPTAC slides, licence per collection), the Cell Image Library, Wellcome Collection, Wikimedia Commons…

