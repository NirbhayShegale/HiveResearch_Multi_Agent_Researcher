# ── Backend Dockerfile ────────────────────────────────────────────────────────
FROM python:3.12-slim

# libpq-dev for psycopg binary
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests (layer-cache friendly)
COPY pyproject.toml uv.lock ./

# uv creates the venv at /app/.venv
RUN uv sync --frozen --no-dev --no-install-project

# Copy project source
COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Use absolute path — no PATH resolution needed, guaranteed to work
CMD ["/app/.venv/bin/uvicorn", "UI.Backend:app", "--host", "0.0.0.0", "--port", "8000"]
