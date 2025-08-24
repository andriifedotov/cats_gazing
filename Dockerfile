FROM python:3.11-slim

# Environment for lean, predictable Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./app.py
COPY templates ./templates
COPY static ./static

EXPOSE 5000
USER appuser

# Gunicorn for production-ish serving
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "-"]
