# ── Backend Dockerfile ────────────────────────────────────────────────────────
FROM python:3.12-slim

# System dependencies required by psycopg binary
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first (layer-cache friendly)
COPY pyproject.toml uv.lock ./

# uv sync creates a .venv at /app/.venv — put its bin/ on PATH
RUN uv sync --frozen --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Copy the full project AFTER deps (better layer caching)
COPY . .

EXPOSE 8000

# Call uvicorn directly from the venv — no `uv run` wrapper needed
CMD ["uvicorn", "UI.Backend:app", "--host", "0.0.0.0", "--port", "8000"]
