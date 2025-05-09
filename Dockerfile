FROM python:3.12.3-alpine3.18

# Install only essential build dependencies, and remove them after building
RUN apk add --no-cache \
    make \
    gcc \
    curl \
    htop \
    vim \
    net-tools \
    libpq-dev \
    python3-dev \
    build-base \
    && rm -rf /var/lib/apt/lists/*

# Create required folders
RUN mkdir -p /app/statics /app/log/{uwsgi,gunicorn,uvicorn}

# Install uv globally
RUN pip3 install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy only pyproject files before full source for better layer caching
COPY pyproject.toml uv.lock* /app/

# Create venv and sync dependencies with cache
RUN --mount=type=cache,target=/root/.cache \
    uv venv && uv sync

# Copy project files
COPY . /app/

# Create and sync virtual environment
RUN uv venv && uv sync

# Set working directory to your app
WORKDIR /app/zinc_app

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:5000/health/ || exit 1

EXPOSE 5000

# Start the app using Makefile target
ENTRYPOINT ["make"]
CMD ["run-app"]