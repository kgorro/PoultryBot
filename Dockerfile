FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    LLM_STORE=/data/llm_answers.jsonl

WORKDIR /app
COPY backend/requirements-serve.txt backend/
RUN pip install --no-cache-dir -r backend/requirements-serve.txt

COPY . .
# Rebuild the knowledge dump inside the image so it always matches the code and KB it ships with
RUN python kb/build_kb.py && python -m dalan.dump \
 && useradd --system --uid 10001 bot && mkdir -p /data && chown bot /data
USER bot

WORKDIR /app/backend
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
