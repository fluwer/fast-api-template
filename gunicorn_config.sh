#!/bin/bash

sleep 3
alembic upgrade head
gunicorn src.start_gunicorn:app \
  --preload \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornH11Worker \
  --bind=0.0.0.0:8000 \
  --timeout=600 \
  --max-requests=50000 \
  --keep-alive 0 \
  --log-config=src/core/logging.conf \
  --log-level info