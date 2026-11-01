# teardown

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/teardown/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **the object is real and exact**: geometry, positions and counts come from the product's own files (STEP, KiCad, BOM, assembly guide). Nothing is eyeballed that a file can
2. **it is shown apart**: layers float on one axis with even, readable gaps, each still oriented as it sits in the

Materials & rendering:
1. **Boards are painted from their layout files**: copper pours, every trace, via, pad and drill, silkscreen, on both sides, at 14–20 px per millimetre, with roughness, metalness and bump maps from the same drawing. Components stand at their footprint positions…

Motion quality:
1. **Separation**: smooth start, fast middle, long settle (ease-in-out cubed); layers leave top first, 0.15–0.2 s apart; repeated parts (keys, screws) fan out in a wave ordered by distance from a
2. **Closing**: bottom first, quicker (about 1 s per layer), the last layer lands with a real mechanical response (a key travels its stroke and returns; nothing bounces like rubber unless it is

Native moves:
1. **The wave lift.** Repeated parts rise in a wave across the object. *Fits content like:* battery cells; solar tiles; the drawers of a modular
2. **Inside the gap.** The camera enters the space between two lifted layers to see a hidden face. *Fits content like:* the back of a logic board; the inside of a drone arm; the underside of a sensor

Pitfalls of the medium:
1. **Invented numbers.** A size that no file gives. Fix: measure it from the CAD and say "measured" in the facts file, or leave it
2. **Mixed-up revisions.** Plates, cases and boards from different versions of a project. Fix: check hole positions and stack heights across the files (they must coincide), and pin the

