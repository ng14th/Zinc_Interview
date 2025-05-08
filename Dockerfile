FROM python:3.12.3-alpine3.18

# Install only essential build dependencies, and remove them after building
RUN apk add --no-cache \
    make \
    gcc \
    curl \
    htop \
    vim \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create required folders
RUN mkdir -p /app/statics /app/log/{uwsgi,gunicorn,uvicorn}

# Install uv globally
RUN pip3 install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Create and sync virtual environment
RUN uv venv && uv sync

# Set working directory to your app
WORKDIR /app/zinc_app

EXPOSE 5000

# Start the app using Makefile target
ENTRYPOINT ["make"]
CMD ["run-app"]