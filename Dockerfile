# ── Backend Dockerfile ────────────────────────────────────────────────────────
FROM python:3.12-slim

# System deps for psycopg binary
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv via official install script (avoids ghcr.io registry issues)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && uv --version

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Install into system Python — no venv, no PATH tricks
RUN UV_SYSTEM_PYTHON=1 uv sync --frozen --no-dev --no-install-project \
    && uvicorn --version

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "UI.Backend:app", "--host", "0.0.0.0", "--port", "8000"]
