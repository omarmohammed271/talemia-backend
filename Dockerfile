# ── Stage 1: base ─────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps needed by psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Stage 2: dependencies ──────────────────────────────────────
FROM base AS deps

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Stage 3: final image ───────────────────────────────────────
FROM deps AS final

COPY . .

# Remove local .env — config comes from docker-compose environment
RUN rm -f .env

EXPOSE 8000

# Gunicorn: 4 workers, bind to 0.0.0.0:8000
CMD ["gunicorn", "starrise_api.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
