docker build -t my-static-site .
docker run -d -p 8000:8000 --name static-web my-static-site