Web/
├── app/
│   ├── templates/
│   │   ├── create.html
│   │   └── index.html
│   ├── venv/
│   ├── requirements.txt
│   ├── app.py
│   └── Dockerfile
├── nginx/
│   └── nginx.conf/
│       └── nginx.conf
├── services/
│   └── service1/
│       ├── service.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── run.sh
├── docker-compose.yml
├── run_docker.sh
├── README.md
├── run.sh
├── PLANNING.md
├── TASKS.md

--
'docker-compose'
version: '3.8'

services:
  app:
    build: ./app
    volumes:
      - ./app:/app
    expose:
      - "8080"
    networks:
      - app_network

  service1:
    build: ./services/service1
    ports:
      - "5001:5000"
    networks:
      - app_network

  nginx:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf/nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /etc/nginx/ssl-dhparams.pem:/etc/nginx/ssl-dhparams.pem:ro
    depends_on:
      - app
      - service1
    networks:
      - app_network

networks:
  app_network:
    driver: bridge
--

