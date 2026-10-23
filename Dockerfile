# realestate POC: one image, one container (spec section 2). The model key and PII key are mounted read-only
# at runtime from /srv/realestate/secrets; nothing secret is baked into the image.
FROM python:3.12-slim

# Pango/HarfBuzz for WeasyPrint (try-first check T1); fonts for PDF output.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libharfbuzz-subset0 fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY config ./config
COPY fixtures ./fixtures
COPY seed ./seed
COPY replays ./replays
COPY scripts/try ./scripts/try

ENV REALESTATE_DATA_DIR=/data \
    REALESTATE_SECRETS_DIR=/run/secrets/realestate \
    REALESTATE_REVIEW_DIR=/review \
    REALESTATE_LOG_FILE=/data/app.log \
    PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')"
CMD ["uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
