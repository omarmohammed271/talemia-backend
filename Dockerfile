# ── Stage 1: base ─────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

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

# Copy Django project package (includes settings.py, views.py, db.py, urls.py, queries.py)
COPY starrise_api/ ./starrise_api/

# Create dashboards app package
RUN mkdir -p /app/dashboards && touch /app/dashboards/__init__.py

# Copy app files into dashboards/
COPY starrise_api/queries.py  ./dashboards/queries.py
COPY starrise_api/views.py    ./dashboards/views.py
COPY starrise_api/db.py       ./dashboards/db.py
COPY starrise_api/urls.py     ./dashboards/urls.py

# Generate manage.py
RUN printf '#!/usr/bin/env python\nimport os, sys\n\ndef main():\n    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starrise_api.settings")\n    from django.core.management import execute_from_command_line\n    execute_from_command_line(sys.argv)\n\nif __name__ == "__main__":\n    main()\n' > /app/manage.py

RUN rm -f .env

EXPOSE 8000

CMD ["gunicorn", "starrise_api.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]