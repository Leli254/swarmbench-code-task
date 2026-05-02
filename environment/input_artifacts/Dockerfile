# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

# Prevent Python from writing pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    libffi-dev \
    libpq-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy only dependency files to leverage Docker layer caching
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy project source code
COPY . /app/

# Collect static files (optional, can also be run at runtime)
RUN python manage.py collectstatic --noinput

# Stage 2: Production image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libffi7 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Expose Django port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
