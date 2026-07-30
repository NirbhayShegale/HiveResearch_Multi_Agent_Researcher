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

COPY pyproject.toml uv.lock ./

# UV_SYSTEM_PYTHON=1 → installs into system Python, no venv created
# Verify uvicorn is available immediately after install
RUN UV_SYSTEM_PYTHON=1 uv sync --frozen --no-dev --no-install-project \
    && uvicorn --version

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "UI.Backend:app", "--host", "0.0.0.0", "--port", "8000"]
