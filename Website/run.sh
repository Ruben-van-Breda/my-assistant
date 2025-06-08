#!/bin/bash
# This script builds a Docker image for a static website and runs it.
# Ensure you have Docker installed and running before executing this script.
# Stop any existing container
docker stop static-web || true
docker rm static-web || true    
docker build -t static-web .
docker run -d -p 8000:8000 --name static-web static-web
# python3 -m http.server 8000 --directory src