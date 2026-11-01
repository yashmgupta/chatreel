# glass-product

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/glass-product/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Materials & rendering:
1. **Studio = a strip-light scene, not an HDRI.** Photo-studio HDRIs contain windows and clutter that print as messy streaks on glass. Build a tiny black scene of emissive planes and bake it to PMREM **every frame** (the implementation, dispose the previous RT):…
2. **Clear glass**: the implementation, transmission 1, roughness ≈ 0.015, IOR ≈ 1.5, thickness sets lensing (thicker = stronger), **dispersion on** (three r163+), near-neutral attenuation, the implementation so other glass sees its back

Colour logic:
1. **One accent colour family, reserved for light** (emission, caustic rings, the dispersion line on UI), optionally drifting between two neighbouring hues with age or energy. Examples: ice blue → soft violet; amber → rose; green → cyan. Pick it from what the…

Type & subtitles:
1. **Subtitles are a slab of frosted glass**: a centred rounded bar filled with the live frame blurred (the implementation on the WebGL canvas, the implementation), a little cool white, a thin highlight stroke and an accent line on top. A licence-free grotesk…
2. **Titles**: the same grotesk at an ultra-thin weight (200), very large (100–140 px) with very wide tracking, centred in the upper third; a diagonal glint sweeps across the letters in sync with the sweep light on the object. Small tracked caps (18–20 px) for…

Motion quality:
1. **Everything moves on ones** (24 fps), eased: ease-in-out for camera orbits, ease-out for parts decelerating into a float, ease-in for a snap
2. **The camera always drifts**: slow orbits or push-ins; never a locked-off frame, never handheld, except a couple of frames of micro-shake on an

Sound palette:
1. **Minimal electronic, never piano-and-strings.** Timbres, as options: bowed-glass or wet-finger tones, granular crystal clouds, glass bells and FM glass plucks, a filtered tick grid for precision, a warm pad, sub drone, soft short kicks and claps, 808 bass…
2. **Lock every pulse, sweep and snap to the score**: write the cue map first and share one hit list between the score and the renderer; light pulses may follow a syncopated bass pattern

Native moves:
1. **Transparency.** The inside is the hero; rack focus from the shell to the part within. *Fits content like:* a juicer's blades; a watch movement; a supplement capsule's
2. **Lensing.** A thick glass dome magnifies and bends what is behind it; macro through it feels like looking into a jewel. *Fits content like:* a camera module; a magnifying tool; a water

