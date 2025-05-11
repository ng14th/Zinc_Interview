#!/bin/bash

# Step 1: List all Docker services
echo "📋 Listing current Docker services..."
docker service ls

# Step 2: Prompt for service name
read -p "🔧 Enter the service name to scale: " SERVICE_NAME

# Step 3: Prompt for number of replicas
read -p "🔢 Enter the number of replicas: " REPLICA_COUNT

# Step 4: Scale the service
echo "⚙️ Scaling service '$SERVICE_NAME' to $REPLICA_COUNT replicas..."
docker service scale "${SERVICE_NAME}=${REPLICA_COUNT}"

# Step 5: Remove exited containers that start with the service name
echo "🧹 Removing exited containers starting with '$SERVICE_NAME'..."
docker ps -a --filter "status=exited" --format "{{.ID}} {{.Names}}" \
  | awk -v name="^${SERVICE_NAME}" '$2 ~ name {print $1}' \
  | xargs -r docker rm

echo "✅ Done."