# Build stage
FROM python:3.9-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Finaly stage
FROM python:3.9-slim

COPY --from=builder /wheels /wheels
COPY --from=builder /requirements.txt .
RUN pip install --no-cache /wheels/*

COPY start_bot.sh .
RUN chmod +x /start_bot.sh

COPY alembic.ini .
COPY migrations /migrations

COPY bot/ /bot
