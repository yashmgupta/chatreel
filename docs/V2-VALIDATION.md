# Educational renderer v2: validation and practical limits

Validation date: 2026-11-01. See [the research review](RENDERER-RESEARCH.md) and [machine-readable per-template audit](education-audit.json). This document supersedes the original five-style validation for the new educational workflow; the old examples remain available as historical/compatibility artifacts.

## What changed

The first version proved that simple shapes could be encoded, but did not adequately represent educational content. V2 adds 18 semantic templates, six original themes, bundled regular/bold/monospaced fonts, a shared Pillow/Canvas/SVG scene compiler, measured text bounds and collision checks, explicit mathematical data mappings, reading-duration guidance, deterministic motion and static-layer caching. No model weights, model APIs or generated/stock pictures are used.

## Executed checks

- **26 native tests passed** across legacy rendering, educational fidelity and API behavior. The suite includes all 18 template layouts, all portrait layouts, six new themes plus five legacy palettes preserving numeric geometry, random-access deterministic frames, real MP4 encoding, shared-schema/OpenAPI consistency, uploaded voice, encoder/dependency failures, API/body/queue/deadline checks, authenticated and signed downloads, and actual Chromium/TTS/WebGL regressions.
- Educational tests inspect meaningful properties: rendered bar lengths match data within rasterization tolerance, chart scales are linear, donut angles sum to a whole, fraction cells match their numerator/denominator, arithmetic uses restricted Decimal evaluation, rounded results use approximate equality, and literal code indentation is preserved. Inputs containing executable expressions, invalid ranges, inconsistent results, unsupported glyphs or unreadable text fail.
- **36 real template MP4s audited**: 18 Python plus 18 Canvas, each 640×360, 12 fps, five seconds, 60 decoded frames, H.264/AAC and BT.709. All have audio, changing/nonblank representative frames, and zero detected black intervals. All measured **−14.0 LUFS** and **−1.5 dBFS true peak** in this QA set. The measured maximum Python/Canvas mean absolute RGB difference was **2.620/255**; rasterization differs, so this is not a pixel-identity claim.
- Visually reviewed the decoded 18-template gallery, including labels, chart values, basic mechanisms, caption margins and the code example. No claim of full-speed listening or human subject-expert review.
- **A complete 1080p lesson**: `examples/education/solar-lesson.mp4` is 60 seconds, 1920×1080, 30 fps and 1800 decoded frames. It uses five related scenes: opener, energy flow, DC/AC comparison, an explicitly illustrative 2 kW × 3 h = 6 kWh calculation, and a recap. Every scene's representative decoded frame was inspected. Frame/stream checks, black-frame detection and audio measurement were run on the finished file.
- A real **MoviePy 2.2.1 fallback** rendered an equation film with system ffmpeg hidden from the capability report, using its installed encoder. The output passed ffprobe checks. Its normalization is reported unmeasured; the two-pass mastering guarantees apply to the native ffmpeg path.
- The Docker image builds with pinned server dependencies. The documented resource-limited container command runs shared Canvas plus conventional eSpeak speech and verifies the finished MP4, retaining Chromium's internal sandbox and the namespace seccomp profile. The same command is configured in the repository CI workflow.
- The offline kit includes the shared schema, render modules, three licensed font files, template examples and education guide. It is checked after extraction into a fresh directory and renders without depending on the original checkout.

## Reproduce

```sh
python -m unittest discover -s tests -v
python tools/render_education.py
CHROMIUM_EXECUTABLE=/usr/bin/chromium python tools/render_education.py --backend canvas
python tools/audit_education.py
python renderer-py/render.py examples/education/solar-lesson.json --out artifacts/solar-delivery
python tools/package_offline.py
```

Full tests require native Chromium/eSpeak/ffmpeg. The five-second QA clips intentionally shorten some templates' recommended reading holds; they verify rendering, not lesson pacing. Editable template JSONs include longer holds. Browser namespace restrictions require the documented host/container configuration. A Docker build can be large on VFS storage; keep enough disk space and remove obsolete task-owned build artifacts as needed.

## Accuracy boundaries

Software checks geometric/mathematical consistency and output mechanics. It cannot establish that an arbitrary supplied fact, unit, source label or reference URL is correct. Decimal division has finite precision; displayed rounded results are marked approximate. Chart labels are rounded for readability. Line-chart observations are equally spaced; use this template only when that spacing represents the intended observations. Source references in examples are pointers for review, not evidence that their current contents were fetched and verified during rendering.

Solar-energy is a simplified energy flow, not electrical wiring or a complete grid model. Water-cycle selects four processes; it omits other hydrological pathways. Icons are schematic; an atom icon does not represent physical electron trajectories. These limitations are included in GPT knowledge and documentation.

English/Latin-oriented font coverage is tested; unsupported glyphs are rejected. Browser and Python font rasterization differ slightly. SVG text metrics require DejaVu fonts in the viewer. TTS is plain English eSpeak formant synthesis, not neural narration. No pronunciation/ASR verification is included. No live Custom GPT session, public hosted Action, multi-tenant deployment, external source verification or publication-specific editorial approval is claimed.

A video may be mechanically valid and still need content, pacing, accessibility or artistic revisions. The checked-in examples demonstrate a much stronger, inspectable educational workflow; they do not establish universal or “perfect” production readiness.
