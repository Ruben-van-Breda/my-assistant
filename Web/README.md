# My Assistant

This project is a multi-service assistant application, containerized with Docker and orchestrated using Docker Compose. It includes a main web application and additional services, all managed behind an Nginx reverse proxy.

## Project Structure

```
.
├── app/                # Main web application (Flask or similar)
│   ├── app.py
│   ├── Dockerfile
│   └── templates/
├── services/           # Additional microservices
│   └── service1/
│       ├── service.py
│       ├── Dockerfile
│       └── run.sh
├── nginx/              # Nginx configuration
│   └── nginx.conf/
│       └── nginx.conf
├── docker-compose.yml  # Docker Compose configuration
├── run.sh              # Script to run the project
├── run_docker.sh       # Script to run Docker containers
├── PLANNING.md         # Planning notes
├── TASKS.md            # Task tracking
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the Application

1. **Build and start all services:**
   ```sh
   ./run_docker.sh
   ```
   or
   ```sh
   docker-compose up --build
   ```

2. **Access the web app:**
   Open your browser and go to `http://localhost` (or the port specified in `nginx.conf`).

### Stopping the Application

```sh
docker-compose down
```

## Project Components

- **app/**: Main web application (e.g., Flask app)
- **services/**: Additional microservices
- **nginx/**: Reverse proxy configuration

## Development
- Update `PLANNING.md` and `TASKS.md` to track progress and ideas.
- Modify or add services in the `services/` directory as needed.

## License
Specify your license here.
