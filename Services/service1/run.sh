# Stop any existing container
docker stop service1 || true
docker rm service1 || true
docker build -t service1 .
docker run -p 5001:5001 service1