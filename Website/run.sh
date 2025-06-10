#!/bin/bash

service_name="static-web"
port=8080
echo "Building $service_name service"
echo "Using port $port"
echo "----------"
echo "Running $service_name service"
docker stop $service_name || true
# Optional: Remove image after run (if you want full cleanup)
docker rmi $service_name
docker rm $service_name || true
docker build -t $service_name .


echo "Running Python HTTP server on port 8000"
docker run -p 8080:8000 $service_name
# python3 -m http.server 8000 --directory src
# echo "Service $service_name is running on port $port"
