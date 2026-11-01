# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 JOB_DIR=/data/jobs
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg espeak-ng chromium chromium-sandbox fonts-dejavu-core ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server/requirements.txt server/requirements.txt
RUN --mount=type=secret,id=ca_bundle \
    if [ -f /run/secrets/ca_bundle ]; then export PIP_CERT=/run/secrets/ca_bundle NODE_EXTRA_CA_CERTS=/run/secrets/ca_bundle; fi; \
    pip install --no-cache-dir -r server/requirements.txt
ENV CHROMIUM_EXECUTABLE=/usr/bin/chromium
COPY film-schema.json film-schema.json
COPY templates templates
COPY renderer-py renderer-py
COPY server server
COPY LICENSE ATTRIBUTION.md ./
COPY licenses licenses
RUN chmod -R a+rX /app && useradd --create-home --uid 10001 renderer && mkdir -p /data/jobs && chown -R renderer:renderer /data
USER renderer
EXPOSE 8000
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log"]
