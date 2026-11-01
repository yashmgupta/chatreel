# Chatreel roadmap

Chatreel has two rendering paths, 18 educational templates, six new themes and five legacy style ports. These are directions for discussion, not committed releases or hosted features.

## Make the first film easier

- Gather compatibility reports from real ChatGPT Data Analysis sessions.
- Improve failure messages and beginner troubleshooting using those reports.
- Make the example stories more expressive within the existing scene language.

## Improve picture and sound

- Improve the educational illustrations and material grammar of the five legacy style ports.
- Extend bundled-font coverage and text shaping beyond the currently supported scripts.
- Expand MoviePy fallback testing across supported operating systems; a real v2 fallback render now passes locally.
- Consider optional higher-quality server TTS, with clear licensing and resource limits.

## Improve hosting

- Document reproducible HTTPS deployments with sandboxed Chromium.
- Evaluate cancellation, per-user job isolation and external queue/storage support.
- Explore a shared hosted GPT experience; no public hosted service is available yet.

## Grow the style library carefully

Port additional 2D styles only when both backends, small knowledge guides, real clips and frame checks are complete. Keep unsupported reference styles clearly separated from renderable IDs.

Have a concrete use case? [Open a feature request](https://github.com/yashmgupta/chatreel/issues/new?template=feature_request.yml). Include what you want to make and why the existing workflow falls short.
