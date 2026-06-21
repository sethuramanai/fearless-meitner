# Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final minimal image
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

# Copy installed python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application source code
COPY . .

# Create directory for static files collection
RUN mkdir -p /app/staticfiles

# Collect static files during docker build
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run using gunicorn for production
CMD ["gunicorn", "todo_project.wsgi:application", "--bind", "0.0.0.0:8000"]
#CMD sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn todo_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}"

