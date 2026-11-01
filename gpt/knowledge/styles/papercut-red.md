# papercut-red

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/papercut-red/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Paper grain:** a neutral-grey texture in the implementation inside each piece (dye mottling, fibres, specks), then the piece's alpha restored with the implementation, so holes stay
2. **Cut edge:** every silhouette is a polyline with a slight low-frequency wobble (hand-cut), a 1 px light rim upper-left and a dark rim lower-right (the cut face). Architecture and machines use straight segments + wobble, never

Colour logic:
1. **China red** (around the implementation, range the implementation–the implementation) is the hero material. Depth and role are shown by **paper tones one step apart**, not by shading: near pieces one step brighter, far pieces one step darker, an antagonist…
2. **Ground and hero must be different paper families.** If background and hero are both red, the silhouettes stop popping. At night, all background layers are one dark dyed family and only the pieces that matter to the story are red; by day, a light paper…

Type & subtitles:
1. **Subtitles are a paper strip in the world**, e.g. a red banner (横批) darker than the picture's reds so cream text holds, serrated edges, swallow-tail ends; a sturdy OFL serif (e.g. Fraunces SemiBold) around 44 px, low, with a paper shadow. It drops in on two…
2. **Titles** are cut-out letters (*yang*-cut, counters are real holes) popping in letter by letter on 12 fps steps, with sawtooth border strips and a seal cut by

Motion quality:
1. **Characters step at 12 fps** (pose sampled at the implementation); **camera, light, weather, flames and flying pieces move on ones** at 24
2. **Folding:** the flap is split into ~16 strips; each is compressed by cosθ and enlarged along the fold by the implementation (fake perspective), darkened as it stands up, in a lighter back colour past 90°, with a growing shadow and a crease after. About half…

Sound palette:
1. **Foley follows the material:** scissors = metallic shear sweep (2.5–9 kHz) + a short ring + a fibre crack; folds = swish + crease tap; unfold = sharp snap; heavy steps = *cardboard* thud, not flesh; paper peel; pasting = a palm pat; match strike, puff;…
2. **Instruments:** a bright Chinese chamber ensemble, not piano and strings and not the opera percussion of shadow puppetry: pipa (tremolo on long notes), zheng (the implementation: broken chords, glissandi, tremolo), erhu (glides), dizi (flute), sheng or…

Native moves:
1. **Fold – cut – unfold.** Fold a sheet 2/4/8 times; one cut becomes many. Put the unfold on a strong beat. *Fits content like:* one teacher, many students; a single design mass-produced; one seed becoming a
2. **Holes are light.** A cut-out lit from behind glows deep red, every hole glows, and the pattern is projected onto the world. *Fits content like:* an idea shining through a person; a lighthouse; a window at night in a story about

Pitfalls of the medium:
1. **Red on red** reads as one blob → different ground family, near/far paper tones, inset contours for
2. **Darkening a layer through the light map** also darkens what covers it → tint the layer itself (multiply + restore

