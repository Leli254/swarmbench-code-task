# Use Python 3.11-slim as the base
FROM python:3.11-slim

# Set the working directory to /workspace as per Harbor standards
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy input artifacts from the current build context
COPY ./input_artifacts/ /workspace/input_artifacts/

# Install Python dependencies with increased timeout and retries
# Added --default-timeout to handle jittery connections
RUN pip install --no-cache-dir --default-timeout=100 \
    pytest \
    pandas \
    requests \
    pillow \
    psycopg2-binary \
    django \
    stripe

# Set the entry point to bash
CMD ["/bin/bash"]