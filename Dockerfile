# syntax=docker/dockerfile:1
FROM python:3.12-slim-trixie

ARG VERSION=dev
ARG REVISION=unknown
LABEL org.opencontainers.image.title="InBraille" \
      org.opencontainers.image.description="Text to Braille converter with STL export for 3D printing" \
      org.opencontainers.image.source="https://github.com/lucasrguerra/InBraille" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=3000 \
    # The container is only reachable through the reverse proxy, so trust its X-Forwarded-For
    # (needed for per-client rate limiting).
    FORWARDED_ALLOW_IPS="*"

WORKDIR /app

# Runtime libraries required by VTK.
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libosmesa6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# --prefer-binary: never compile from source (required on ARM64 where some wheels are missing)
# pip/setuptools (and the libraries vendored inside pip) are build tools: remove them from the runtime image.
RUN pip install --upgrade pip && pip install --prefer-binary -r requirements.txt \
    && pip uninstall -y pip setuptools wheel

COPY main.py index.html google21a790a2c23c0ec5.html ./
COPY src ./src
COPY public ./public

RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin inbraille
USER 10001

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import os,urllib.request as u; u.urlopen('http://127.0.0.1:%s/' % os.environ.get('PORT','3000'), timeout=5)"]

CMD ["python", "main.py"]
