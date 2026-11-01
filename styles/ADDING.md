# Add a style
1. Copy TEMPLATE.md; define invariants independently of any demo plot. Record attribution.
2. Add its ID to film-schema.json, render.py STYLES, Canvas style branches and /styles metadata. Keep both engines deterministic for random-access render(t).
3. Implement material-specific geometry and transitions in both backends. Do not accept caller code or URLs. Reserve captions outside actor space.
4. Add a condensed knowledge file and update supported-style instructions. Keep unavailable reference styles clearly marked.
5. Render five seconds in both modes, inspect beginning/middle/end frames and motion differences, verify duration/audio, and extend tests. Record limitations in docs/VALIDATION.md before advertising support.
