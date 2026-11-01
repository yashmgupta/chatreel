# paper-lantern

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/paper-lantern/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. 1. **A paper layer**: a flat cut sheet, one flat colour, fibre grain, a thin warm **rim of light on its top edge** and a **dark band on its bottom edge**. Back layers lighter and cooler, the front almost black: that value ladder *is* the
2. 2. **Light through paper**: a warm, cloudy translucency (pulp mottling), strongest near the light source. Windows, lanterns, trails of light are **holes / emissive windows** that burn and

Materials & rendering:
1. **Units in metres, y up.** Layers from z ≈ −0.14 (sky) to 0 (front); camera at z ≈ 0.2–0.56, fov ~26°. In box framing, sheets are **never larger than the cavity**. In full-bleed shots that travel, a layer may be a long strip that scrolls past, and the sky…
2. **A layer** is a Canvas2D drawing in metre space mapped to a plane; cut-outs are the implementation holes. Finish on every sheet: fibre grain (the implementation), a warm top rim and a dark bottom shade, each shifted a few

Colour logic:
1. **Back layers bright and translucent, front layers dark and opaque.** Each layer is one flat colour; the ladder of values from back to front is the depth. Never break it (a pale front layer flattens the
2. **One temperature per stack**, chosen by the scene (cool night, warm interior, violet or green elsewhere). Changing ladder is how the film says "another

Type & subtitles:
1. **Text in the picture is paper**: titles, letters, poems and captions are cut strips inside the box, revealed by growing from an anchor edge (scale the texture repeat with the mesh so glyphs aren't squashed), with an optional small
2. **Subtitles** are quiet and burned in: warm off-white serif, soft shadow, fading in just before the line. Where they sit depends on the

Motion quality:
1. **Everything moves like paper on a stick**: layers slide (x/y), rotate about a pivot, scale in from 0 along one axis ("written out"), or light up. No squash and stretch, no morphing, no
2. **Figures are optional.** A film can tell its story with lit windows, vehicles, lamps and objects, and have no figure at all. When it has figures, they are jointed silhouettes: a body sheet + separate limb sheets anchored at the joint; animate rotation

Sound palette:
1. **Instruments** that sit like light behind paper: felt piano, music box, celesta, harp or plucked zithers, bamboo flutes, soft strings; a solo instrument of the topic's culture. No drum kit; percussion only as single soft strokes (woodblock, small gong, hand…
2. **Foley is paper and light**: switch click + rising shimmer when a light turns on; paper rustle and slide; card-stock tap; lid thud; chimes on reveals; soft whoosh for curtains; beds from the scene (river, rails, city hum, crickets, snow

Native moves:
1. **The lamp turns on.** Source, then far layers, then windows light up one by one. *Fits content like:* a shop opening at dawn; a startup's first customer; a stadium before a
2. **Two windows, one light.** Two lit places sharing one light source (a moon, a lighthouse, a satellite). *Fits content like:* a long-distance friendship; two labs working on the same problem; a sister city

Pitfalls of the medium:
1. **Grade state must not carry over** between shots: every grade key a shot omits must fall back to a default each frame, or renders depend on which frame a worker started on (visible pops at worker
2. **Light over paper text**: a lamp's glow or a headlight flare over a name board or a card washes the letters out. Keep every lit point clear of

