# Use a slim Python image to keep the environment lightweight but functional
FROM python:3.11-slim

# Set the working directory inside the container
# Harbor tasks typically operate out of /workspace
WORKDIR /workspace

# Install essential system-level dependencies
# - git: Required if the agent needs to track changes or apply patches
# - build-essential: Necessary if any Python packages need to compile C extensions
# - curl: Useful for downloading additional assets if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the input artifacts  into the container
COPY input_artifacts/ /workspace/input_artifacts/

# Install Python-specific dependencies
# We include 'pytest' as it is the standard for the verifier script.
RUN pip install --no-cache-dir \
    pytest \
    pandas \
    requests


CMD ["/bin/bash"]