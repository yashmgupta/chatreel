# Contributing to Chatreel

Thanks for helping people make code-rendered films from a conversation. Small, focused contributions are welcome. Read [the README](README.md), [known limitations](README.md#known-limitations) and [attribution](ATTRIBUTION.md) before changing an engine or guide.

## Useful first contributions

These are suggested tasks, not already-created or assigned GitHub issues:

- Improve one confusing sentence in the ChatGPT quick start after trying it yourself.
- Share a reproducible sandbox compatibility report: available libraries, encoder and outcome, without personal files or secrets.
- Add a short original film JSON that uses the current schema, with attribution and reviewed frames.
- Improve caption contrast or spacing for a specific style, with before/after screenshots.
- Document a supported deployment host's Chromium sandbox configuration.

For a new renderer feature or style, open a feature request first so its scope and fit can be discussed. For a small fix, a focused pull request is enough.

## Develop and validate

Use Python 3.11+ and the existing checkout. Installation instructions are in the README. For the complete suite, install `server/requirements.txt`, `tests/requirements.txt`, Chromium, eSpeak NG and ffmpeg. Set `CHROMIUM_EXECUTABLE` if using system Chromium.

```sh
python -m unittest discover -s tests -p test_render.py -v
# Full suite: includes real Chromium jobs and needs its sandbox prerequisites.
python -m unittest discover -s tests -v
```

For visual changes, render the affected styles, decode frames from the MP4s and inspect captions, silhouettes, clipping and motion. `tools/render_education.py` renders the educational templates; run it with `--backend canvas` for browser clips, then `tools/audit_education.py` checks encoded outputs and backend agreement. The legacy tools remain available for old styles. Describe what you actually ran; do not mark browser checks passed when only offline checks ran.

If the README, schema, renderer or bundled license files change, refresh the upload kit:

```sh
python tools/package_offline.py
```

Include the resulting `gpt/chatreel-offline.zip` when its contents changed. Do not commit `.env`, keys, local job folders or logs containing personal data.

## Add a style

Follow [styles/ADDING.md](styles/ADDING.md) and use [the template](styles/TEMPLATE.md). A supported style needs both Python and Canvas implementations, shared-schema support, a small GPT knowledge guide, real test clips and frame review. Reference prompts alone do not count as a renderer port.

Keep frame rendering deterministic. Accept declarative film data, never caller-provided JavaScript, Python, paths or remote asset URLs. Keep original music and code-rendered pictures; video-generation models and stock footage are outside the project's scope.

## Pull requests

Explain the problem, changed behavior and relevant validation. For visual changes, include representative before/after frames and known tradeoffs. Keep unrelated refactors separate. Use the PR template as a checklist, not as a request to run irrelevant checks.

By contributing, you agree to license your original code under MIT and adapted style knowledge under the project's documented CC BY 4.0 terms. Identify external sources and their licenses; retain Lemomo/LemoLab attribution and applicable third-party notices. Submit only material you have permission to share.

Be kind, specific and constructive. Discuss the work, respect different experience levels, and do not post private information.
