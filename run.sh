#!/bin/bash

# Path to the docker-compose.yml file
COMPOSE_FILE="devops/docker-compose.yml"

# Path to the .env file
ENV_FILE="devops/docker.env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    echo "Create a new one using the following command: cp $ENV_FILE.example $ENV_FILE"
    exit 1
fi

docker-compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up --build --force-recreate || {
  echo "Failed to run the bot with docker-compose"
  exit 1
}
