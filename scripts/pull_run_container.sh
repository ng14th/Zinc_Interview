#!/bin/bash

# Set variables
NEW_IMAGE_NAME="nguyennt63/zinc_app:latest"
OLD_IMAGE_NAME="nguyennt63/zinc_app:latest"
BACKUP_IMAGE_NAME="nguyennt63/zinc_app:backup"

CONTAINER_NAME="zinc_app_container"
ENV_FILE="zinc_app/envs/.env"

# Get env variables
set -o allexport
source zinc_app/envs/.env
set +o allexport

# Backup current image
echo "Backing up current image..."

docker tag $OLD_IMAGE_NAME $BACKUP_IMAGE_NAME
# Remove old image
echo "Remove current image..."
docker rmi $OLD_IMAGE_NAME

# Stop and remove old container if exists
echo "Stopping and removing old container..."
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# Pull new image
echo "Pulling new image... $NEW_IMAGE_NAME"
echo "$TOKEN_DOCKER_HUB" | docker login -u "$USER_DOCKER_HUB" --password-stdin && docker pull "$NEW_IMAGE_NAME"

# Run new container
echo "Starting new container..."
docker run -d --restart=on-failure --env-file "$ENV_FILE" -p 5000:5000 --name $CONTAINER_NAME $NEW_IMAGE_NAME

# Wait a bit for container to boot and healthcheck to register
echo "Waiting for container to initialize..."
sleep 5

# Check container health status
HEALTH_STATUS=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME 2>/dev/null)

if [[ "$HEALTH_STATUS" != *"starting"* ]]; then
  echo "Health status: $HEALTH_STATUS"
  echo "🚨 New container is unhealthy. Rolling back..."

  # Stop and remove bad container
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME

  # Re-tag backup image and restart container
  docker tag $BACKUP_IMAGE_NAME $OLD_IMAGE_NAME
  docker run -d --restart=on-failure --env-file "$ENV_FILE" -p 5000:5000 --name $CONTAINER_NAME $OLD_IMAGE_NAME

  echo "✅ Rolled back to previous image."
else
  echo "✅ New container is healthy. Cleaning up backup..."
  docker rmi $BACKUP_IMAGE_NAME
fi
