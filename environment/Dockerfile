# Use Python 3.11-slim as the base
FROM python:3.11-slim

# Set the working directory to /workspace as per Harbor standards
WORKDIR /workspace

# Install system dependencies
# libpq-dev: Required for PostgreSQL (E-soko database)
# libjpeg-dev/zlib1g-dev: Required for Pillow (E-soko thumbnails)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy input artifacts from the environment subfolder
# Note: In your structure, these are in environment/input_artifacts/
COPY input_artifacts/ /workspace/input_artifacts/

# Install Python dependencies
# We add 'pillow' for product images and 'psycopg2-binary' for DB connectivity
RUN pip install --no-cache-dir \
    pytest \
    pandas \
    requests \
    pillow \
    psycopg2-binary \
    django \
    stripe

# Set the entry point to bash
CMD ["/bin/bash"]