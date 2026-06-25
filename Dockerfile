FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# GitPython (used by services/codebase_analyzer) requires the git binary at
# import time; python:3.11-slim doesn't ship it, so install it explicitly.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Use Uvicorn to run FastAPI application.
# Honor the platform-provided $PORT (Railway/Render set this) and default to 8080
# for Cloud Run / local runs.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
