# Add an educational template

1. Describe a specific teaching purpose and the minimum truthful input. Keep reference data and domain simplifications visible; do not reuse an unrelated icon as a substitute for the subject.
2. Add a template ID and description to `education.TEMPLATES`, then add typed fields to `film-schema.json` and regenerate the matching Film schema in `openapi.yaml`. Extend `validate_content` for semantic invariants, limits and failure messages.
3. Build the scene with `Plan` primitives inside `compile_scene`. Use measured text blocks, safe title/caption/source regions, shared theme colors and explicit animation times. Avoid caller code, paths or asset URLs. The same commands already feed Pillow, Canvas and SVG; do not create a second independent layout implementation.
4. Provide a complete `templates/<id>.json` with a realistic reading hold. Add it to `index.json`, the template README and EDUCATION knowledge. Use original procedural graphics and properly licensed bundled assets only.
5. Test what the visual asserts: data-to-geometry proportions, numeric correctness, constraints and layout at wide/portrait sizes. Render a Python and a real Canvas clip, decode their frames, inspect text and compare the outputs. A nonblank-frame assertion alone does not establish educational correctness.
6. Run relevant regression checks, rebuild the upload ZIP and document any remaining content, font, pacing or scientific limitations. New themes are palette options, not a claim to replicate a full physical material engine.
