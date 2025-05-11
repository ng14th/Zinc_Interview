#!/bin/bash

# Set variables
IMAGE_NAME="nguyennt63/zinc_app:latest"
CONTAINER_NAME="zinc_container"
ENV_FILE="zinc_app/envs/.env"
STACK_NAME="zinc_app"

# Get env variables
set -o allexport
source zinc_app/envs/.env
set +o allexport

# Remove old image
echo "Removing current image..."
docker rmi -$IMAGE_NAME

# Stop and remove container
echo "Stopping and removing old container..."
docker container rm $CONTAINER_NAME
docker container ps  # To confirm services are removed

# Pull new image
echo "Pulling new image... $IMAGE_NAME"
echo "$TOKEN_DOCKER_HUB" | docker login -u "$USER_DOCKER_HUB" --password-stdin && docker pull "$IMAGE_NAME"

# Deploy new stack with the new image
echo "Deploying new stack..."
docker stack deploy -c docker-compose-stack.yml $STACK_NAME
