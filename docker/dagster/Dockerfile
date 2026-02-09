# Dockerfile para Dagster.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

ENV PYTHONPATH=/app/src

CMD ["dagster", "dev", "-f", "src/orchestration/definitions.py", "-h", "0.0.0.0", "-p", "3000"]

