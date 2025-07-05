#!/bin/bash
# Build and run the Docker Compose stack with configurable port and service name

# Set default values if not provided
: "${PORT:=8080}"
: "${SERVICE:=nginx}"

echo "Exposing port $PORT for service $SERVICE"

docker-compose down 


docker-compose build
# Run only the specified service and map the port

docker-compose up -d $SERVICE

echo "Service $SERVICE is running on port $PORT"
