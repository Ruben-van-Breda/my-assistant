#!/bin/bash

service_name="chatgpt_service"
port=5002
echo "Building $service_name service"
echo "Using port $port"
echo "----------"
echo "Running $service_name service"
echo "Stopping and Removing old image if exists"
docker ps -a | grep $service_name && echo "Service $service_name is running, stopping and removing old container" || echo "No old service found, continuing"
docker ps -a | grep $service_name && docker stop $service_name || echo "No old service found, continuing"
docker ps -a | grep $service_name && docker rm $service_name || echo "No old service found, continuing"
docker stop $service_name || true
docker rm $service_name || true
# Optional: Remove image after run (if you want full cleanup)
docker rmi $service_name

docker build -t $service_name .
echo "Service $service_name is running on port $port"

docker run -d --name $service_name -p $port:$port $service_name
# echo "Running Python HTTP server on port $port"
# python3 -m http.server 8000 --directory src
