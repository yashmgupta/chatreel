# white-model

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/white-model/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The model is real geometry of a real place**: building footprints and heights from open data (§2), extruded at a stated scale (1:1000, 1:2000…). Nothing on the model is invented or "representative", and no generated image ever stands in for the
2. **The model is white; data is light.** Colour is never painted into the material: it is projected, so it brightens surfaces that face the projector, fades on walls turned away, stops at the edge of the throw and reaches a little onto the

Materials & rendering:
1. **Model**: matte white (≈ #F3F3F1, roughness ≈ 0.9), crisp edges; water a darker satin inlay in the base plate; bridges low white slabs; a thin base plate on a dark satin
2. **Light model**: house light = one soft key + a neutral studio environment + AO on close shots. Projection = a term added to the lit surface in the shader: the implementation, scaled by albedo, reduced on water. Never a texture on the

Colour logic:
1. **One hue family per layer**, chosen for the data: a single categorical accent for "the old/the exception" (e.g. warm amber), a sequential ramp for continuous data (blue → cyan → white for time, violet → magenta → peach for
2. **A colour may return** only with the same meaning (the "before" colour reused later marks the same set of

Type & subtitles:
1. **Roles**: a light grotesk for the figure (Inter Tight 200, 120–140 px), a sans for labels in the film's language (Noto Sans SC 300/500, 20–36 px), a monospace for instruments, years and coordinates (IBM Plex Mono, 18–22 px). OFL, self-hosted, CJK
2. **Readout in the left third**, one per layer: index + layer name, one figure, one label, one source line, a legend

Motion quality:
1. **Light is the actor.** Each layer arrives by a soft-edged gesture of light: a wash spreading from the projector axis, buildings switching on one by one with a short flash, a level climbing every facade, the sun's clock running. No hard line sweeping the…

Sound palette:
1. **The room**: room tone, the projector fan (hum + filtered air) rising when the lamp strikes, relays for the house lights, a lamp strike (zap + thump), the air of a light wash (sliding band-passed
2. **Light as sound**: mallets and glass for things switching on, bowed vibraphone for held light, a rising mallet line and air riser for a climbing level, one glass note per highlighted

Native moves:
1. **Lights out, lamp on.** House light, a relay, darkness, the lamp strikes, the first layer arrives. *Fits content like:* a site before and after; a district before a plan is shown; any "now look
2. **The hole.** Light only the set that answers a question (built before a date, owned by one party, inside a zone) and let the absence draw the shape. *Fits content like:* a war-damaged centre; a flood plain with no housing; land a company owns; a protected…

Pitfalls of the medium:
1. **Wall normals** wound the wrong way show inside faces (walls look hollow): derive the outward normal from ring orientation. **Shared walls** between parts z-fight: skip the overlap below the lower
2. **Warm HDRIs turn the white model beige**: use a neutral studio

