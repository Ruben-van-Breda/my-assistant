# My Assistant

This project is a multi-service web application built with Flask, containerized with Docker, and orchestrated using Docker Compose. It provides a platform for creating and managing web applications with features like authentication, file management, and integration with various microservices.

## Architecture Overview

The application follows a microservices architecture with the following components:

- **Main Web Application (Flask)**: Handles core functionality, routing, and user management
- **Microservices**: Specialized services for specific functionalities
  - Base Chat Service: General purpose chat agent
  - HTML Service: Application builder service
- **Nginx**: Reverse proxy for routing requests to appropriate services

## API Endpoints

### Core Endpoints

- `GET /`: Main application index
- `GET /home`: User's home page (requires authentication)
- `GET /create`: Project creation page (requires authentication)

### Authentication

- `GET /login`: Login page
- `POST /login`: Handle login (email + password)
- `GET /logout`: Logout user

### Project Management

- `GET /get_file_content`: Retrieve content of a project file
  - Query params: `path` (file path)
  
- `POST /save_project_file`: Save/update project file
  - Body: `{ path: string, content: string }`

- `POST /save_html`: Save generated HTML content
  - Body: `{ html: string, save: boolean, filename: string }`
  
- `POST /delete_file`: Delete a project file
  - Body: `{ filename: string }`

### Configuration

- `GET /services_config`: Retrieve services configuration

## Available Services

The application integrates with the following microservices:

1. **Base Chat (Agent Chat)**
   - Purpose: General purpose chat functionality
   - Development URL: http://127.0.0.1:3000/query
   - Production URL: https://my-assistant.co.za/base_chat/query

2. **HTML Service (App Builder)**
   - Purpose: Application building and generation
   - Development URL: http://127.0.0.1:5003/query
   - Production URL: https://my-assistant.co.za/html_service/query

## Project Structure

\`\`\`
.
├── app/                # Main web application
│   ├── app.py         # Core application logic
│   ├── components/    # Reusable components
│   │   └── auth.py   # Authentication module
│   ├── static/       # Static assets
│   │   ├── generated/
│   │   └── projects/ # User project files
│   ├── templates/    # HTML templates
│   └── services.config.json # Services configuration
├── services/          # Microservices
│   ├── base_chat/    # Chat service
│   ├── html_service/ # App builder service
│   └── service1/     # Template service
├── nginx/            # Nginx configuration
├── docker-compose.yml
├── run.sh            # Script to run the project
└── run_docker.sh     # Script to run Docker containers
\`\`\`

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.x (for local development)

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
   Open your browser and go to `http://localhost:8080`

### Development Setup

1. **Create and activate virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r app/requirements.txt
   ```

3. **Run the application locally:**
   ```sh
   python app/app.py
   ```

### Authentication

The application uses a simple authentication system:
- Users can log in with their email address
- Session-based authentication is implemented
- Protected routes require authentication

## Development Guidelines

1. **File Management**
   - User files are stored in `app/static/projects/{user_id}/`
   - Each user gets their own isolated project space
   - Templates and static assets are copied to user directories

2. **Adding New Services**
   - Add service configuration to `services.config.json`
   - Create new service directory in `services/`
   - Update `docker-compose.yml` with new service

3. **Security Considerations**
   - All file operations are restricted to user's project directory
   - File paths are sanitized using `secure_filename`
   - Session-based authentication for protected routes

## Docker Configuration

The application uses Docker and Docker Compose to orchestrate multiple services. Each service runs in its own container, with Nginx acting as a reverse proxy to route requests appropriately.

### Service Architecture

1. **Main Application (app)**
   - Flask application serving the main web interface
   - Built from `./app` directory
   - Internally exposed on port 8080
   - Accessible through Nginx

2. **Base Chat Service**
   - Chat functionality service
   - Built from `./services/base_chat`
   - Exposed on port 3000
   - Accessible at `/base_chat/` endpoint

3. **HTML Service**
   - Application builder service
   - Built from `./services/html_service`
   - Exposed on port 5003
   - Accessible at `/html_service/` endpoint

4. **Nginx (Reverse Proxy)**
   - Routes requests to appropriate services
   - Exposed on port 8080 (host machine)
   - Handles SSL termination in production
   - Configured via `./nginx/nginx.conf/nginx.conf`

### Network Configuration

- All services run on a custom bridge network (`app_network`)
- Internal service communication uses Docker DNS resolution
- Services can reference each other using their service names as hostnames

### Volume Mounts

1. **Application Code**
   - `./app:/app` - Live code updates for development

2. **Nginx Configuration**
   - `./nginx/nginx.conf/nginx.conf:/etc/nginx/nginx.conf:ro` - Nginx configuration
   - `/etc/letsencrypt:/etc/letsencrypt:ro` - SSL certificates (production)
   - `/etc/nginx/ssl-dhparams.pem:/etc/nginx/ssl-dhparams.pem:ro` - SSL parameters

### Running with Docker

1. **Development Mode**
   ```sh
   # Build and start all services
   docker-compose up --build

   # Start in detached mode
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

2. **Production Mode**
   ```sh
   # Build and start with production configuration
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Managing Services**
   ```sh
   # Stop all services
   docker-compose down

   # Restart a specific service
   docker-compose restart service_name

   # View service logs
   docker-compose logs -f service_name
   ```

### Service Dependencies

- The Nginx service depends on:
  - app (Flask application)
  - base_chat
  - html_service
- Services will be started in the correct order automatically

### Accessing Services

- Main Application: `http://localhost:8080`
- Base Chat Service: `http://localhost:8080/base_chat/`
- HTML Service: `http://localhost:8080/html_service/`

## License

Specify your license here.