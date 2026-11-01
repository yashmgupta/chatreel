# Educational renderer research and design review

Studied source on 2026-11-01. This is a focused comparison of four established Python projects, not a claim to have reviewed every GitHub repository. No implementation code from these projects is copied; the new renderer is an original implementation of general animation/rendering techniques. Existing upstream Lemo attribution remains.

| Project / inspected commit | Files studied | Useful engineering practice | Chatreel decision |
|---|---|---|---|
| [Manim Community](https://github.com/ManimCommunity/manim), `16ea443e2a5f1d79db0a721161411ce916d6e733` (MIT) | README, animation/animation.py, animation/composition.py, utils/rate_functions.py, mobject/text/text_mobject.py, scene/scene_file_writer.py | Separate scene construction from timeline interpolation; normalize progress; compose animations with explicit start/end times; account for font shaping and line spacing | Compile declarative educational scenes into a shared display list; evaluate at exact frame times; staged reveals plus readable holds; bundled font and explicit text bounds. Avoid mandatory Manim/Pango/LaTeX installation in the offline sandbox. |
| [MoviePy](https://github.com/Zulko/moviepy), `211e4b15f6ce4f34a6a9efbfff40590e43a68f77` (MIT) | README, Clip.py, video/VideoClip.py, video/compositing, video/io/ffmpeg_writer.py | Time-indexed frames, layers, explicit durations, encoder pixel formats, output cleanup; v2 API differs from v1 | Preserve random-access frame functions and streaming; make frame count/size checks explicit; keep MoviePy optional. |
| [drawsvg](https://github.com/cduck/drawsvg), `832f7fe05027afb2c812bee88fc4eb3242952c86` (MIT) | README, drawing.py, elements.py, native_animation/synced_animation.py | Semantic vector elements, shared viewBox, synchronized attribute timelines, ordered key times | Add SVG export from the same drawing commands used for video; keep charts, labels and connectors in one coordinate system, with no caller-provided SVG/JS. |
| [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg), `be2a02bdeaa728047df3822fa14db2aee0bed4ff` (BSD-2-Clause) | README, imageio_ffmpeg/_io.py and _utils.py | Exact frame buffers, rational frame rates, codec checks, explicit stream mapping and subprocess lifecycle; warns about implicit resizing | Validate RGB sizes and counts, preserve even output dimensions, check the finished file, and avoid implicit resizing. |

## What was wrong with the first version

1. A circle and rectangle could be narrated as solar panels without actually showing a solar panel or explaining electricity. Tests proved encoding, not educational fidelity.
2. Python and Canvas independently implemented layout. This allowed visual differences and doubled the maintenance surface.
3. Character-by-character wrapping could split words; reducing text to a tiny size hid layout problems.
4. No reusable semantic templates, number-to-geometry mapping, arithmetic verification or lesson-specific illustrations existed.
5. A static “tests passed” badge was weak evidence for current changes. Validation must distinguish render mechanics, mathematical checks, visual review and actual domain truth.

## Revised quality contract

- Template data determines the picture: supplied labels, quantities, expressions, units and references are inspectable. Numbers drive bar lengths, point positions, fractions and donut sectors; they are not decorative labels.
- A common scene compiler drives Pillow, browser Canvas and inspectable SVG. Styles change palettes; they do not alter mathematical values.
- No text silently shrinks below the readable design threshold; overflow fails preflight with an actionable error. Titles, footers and captions have distinct safe areas.
- Exact frame-aligned scene durations, deterministic interpolation, antialiasing, bundled font metrics and explicit output profiles improve reproducibility.
- Validation catches mathematical/layout/encoding errors. It cannot prove arbitrary scientific claims or user-provided source accuracy. Educational examples identify simplifications and illustrative datasets. A subject expert still reviews a film intended for publication.
- All frames, music, icons and optional eSpeak speech are generated through conventional code. No inference weights, image/video models, model APIs, stock footage or automatic internet downloads are required by rendering.
