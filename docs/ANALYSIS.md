# Upstream analysis — phase 1

Source: [Lemomo / LemoLab, lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), commit `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00`, inspected 2026-11-01.

## Pipeline and contracts

README describes a style library rather than a fixed video generator. DIRECTOR asks for a brief, three candidate treatments, one subject/goal/turn, a hook, a medium-native signature move, shot list, beat sheet and sound table. Style invariants constrain the film; demo plots must not become templates. Storyboard review is optional upstream; this adaptation requires confirmation.

TECHNIQUE makes one timeline the source of truth for picture, voice placement, score, foley and captions. A project page exposes deterministic `window.render(t)`, `DUR`, `READY`, optional `EV` sound events and `TEXTS` text bounds. Canvas 2D, three.js r170 and WebGL2 shaders draw frames without generated video. `core/render/page.mjs` serves the project/library, `video.mjs` assigns frame ranges to browser workers, captures JPEGs and pipes to ffmpeg H.264. Locks prevent output collisions; seeded randomness permits independent frame evaluation. `still.mjs`, `sheet.py` and `readcheck.mjs` support review.

Voice precedes final animation: Kokoro ONNX local English (downloaded model/voices), edge-tts online Chinese, or user recordings. `asr_check.py` uses faster-whisper for text checks and word timing. Music events share the timeline: `sampler.py` loads VSCO2 CE, VCSL, FreePats, Karoryfer and Salamander; `pluck.py` uses Karplus–Strong/numba, numpy synthesis handles chips/drones. `sfx.py` supplies procedural material sounds. Compress voice, duck music/foley, pan transients, export SRT and paint captions in-frame. `mux.sh` validates audio and uses two-pass ffmpeg loudnorm (-14 LUFS, -1.2 dBTP), pads short audio and encodes the MP4. Upstream requires ffmpeg 7+ due to a reported older loudnorm duration issue.

Review includes contact sheets, key-action strips at 0.2 s, readable text, no blank/NaN frames, loudness and final voice verification. Delivery includes MP4, poster, SRT, treatment, credits and reproducible source.

## Agent/platform dependencies

`plugin/skills/lemo-opuscar/SKILL.md` delegates to AGENTS, DIRECTOR and TECHNIQUE. `scripts/setup.sh` sparse-clones/updates a library, installs tiered npm/Python dependencies, obtains Chromium, and fetches demos on demand. It assumes persistent filesystem, shell execution, subprocesses, package downloads and agent tool questions. Browser capture and GPU/WebGL require an external runtime. Parallel voice/music and multiple frame workers are useful but no mandatory subagent API is part of the film format. Claude's skill installation, AskUserQuestion and automatic filesystem navigation cannot be assumed in a Custom GPT. No browser or internet is assumed in Code Interpreter.

`tools/fetch.sh` checks SHA-256 release-pack manifests, extracts instrument/model/HDRI packs and preserves TLS checks. Release, gallery and directory tools publish/catalogue work; they are not required to render. No large assets or demo voice tracks are reused here.

## Style prompt structure

The catalog includes 66 styles plus `_template`. `upstream-style-inventory.json` records each inspected STYLE.md's hash, headings and initial rules. Common fields: essence/exclusions; material/rendering; palette and colour meaning; typography/subtitles; motion/easing/stepping; camera and transition grammar; sound palette/mix; medium-native moves; pitfalls; reusable engine entry points; variation space. These are constraints, not a prescribed story. Some newer documentary styles explicitly use real footage despite the original code-rendered tagline; they are excluded here.

Selected diverse 2D ports: swiss-motion (grid, paper/ink/one signal colour, exact snaps), blueprint (white orthographic line drawing on Prussian blue, dimensions), chalkboard (clean green board, growing pressure-like strokes, restrained chalk), woodcut (paper margin, black block, form-following carved light), pixel-rpg (low-resolution nearest-neighbour sprites, limited ramps, stepped action). These are deliberately compact interpretations, not pixel-identical replicas of upstream engines. Other prompts are condensed for reference but are not advertised as renderable.

## ChatGPT design decision

Mode A uses trusted Pillow scene objects with a pure `render(t)` method, numpy score, captions or local voice file, and ffmpeg with a moviepy fallback. Missing encoders yield frames/WAV/SRT and an explicit capability report; missing numpy/Pillow yields a clear prerequisite report. It never installs or downloads at runtime.

Mode B accepts the same declarative JSON, renders trusted Canvas code in Playwright Chromium (with an optional WebGL compositing pass), synthesizes speech with local eSpeak, mixes procedural music and encodes with ffmpeg. A bounded persistent SQLite queue, one subprocess worker, deadline, capped film complexity and authenticated result retrieval limit resource use. It accepts neither JavaScript nor remote URLs. Deploy behind HTTPS, with one application worker and persistent job storage. Separate offline and server runtimes; chat itself runs neither browser nor WebGL.

## Licensing

Upstream README says code **and docs** are MIT; demo films/stills are CC BY 4.0 (with three explicitly excluded voice tracks). The request calls styles CC BY 4.0: retain upstream MIT and CC BY legal text and conservatively attribute adapted style material under CC BY 4.0, without claiming upstream docs lacked MIT permission. New code is MIT. Attribution names Lemomo/LemoLab, links upstream and states modifications. Original demo footage, audio, fonts and sample packs are not bundled.
