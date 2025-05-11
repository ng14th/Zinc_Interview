CONTAINER_NAME="zinc_container"
STACK_NAME="zinc_app"

# Remove container
echo "Stopping and removing old container..."
docker container rm -f zinc_container

# Deploy new stack with the new image
echo "Deploying new stack..."
docker stack deploy -c docker-compose-stack.yml $STACK_NAME
