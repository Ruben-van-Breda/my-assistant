Project Overview

We want to create a web application and a separate service, all containerized using Docker, and served via Nginx. The web application will be built with Flask and will have a main index page and an additional route for creating a new page. Separately, we’ll have another service—also using Flask or FastAPI—that will expose a couple of simple endpoints like a “Hello World” route and a query endpoint.

Components:
	1.	Flask Web App:
	•	Main route (/) serving index.html.
	•	Additional route (/create) serving create.html.
	2.	Independent Service:
	•	A simple Flask or FastAPI app with basic endpoints like a “Hello World” route and a query endpoint.
	3.	Docker:
	•	Both the web app and the service will have their own Dockerfiles for containerization.
	4.	Nginx:
	•	Nginx will be configured to expose the main Flask web app on port 8080 and also proxy requests to the separate service. This setup ensures that the main website can communicate with the service, for example, using a fetch call from the /create page.

---

## Next Steps

### 1. Flask Web App
- [x] Scaffold basic Flask app with `/` and `/create` routes.
- [ ] Create `index.html` and `create.html` templates.
- [ ] Add logic to `/create` to interact with the independent service (e.g., fetch from `/service1/hello`).

### 2. Independent Service
- [x] Scaffold Flask service with `/hello` and `/query` endpoints.
- [ ] Add input validation and error handling for `/query`.
- [ ] Consider switching to FastAPI if async or OpenAPI docs are needed.

### 3. Dockerization
- [ ] Write Dockerfiles for both the web app and the service.
- [ ] Ensure both containers run correctly and expose the right ports.

### 4. Nginx Configuration
- [x] Write initial Nginx config to proxy `/` to the web app and `/service1/` to the service.
- [ ] Test proxying and CORS headers if needed.
- [ ] Add SSL/TLS support (optional, for production).

### 5. Orchestration
- [x] Write `docker-compose.yml` to coordinate all services.
- [ ] Add healthchecks for containers.
- [ ] Document environment variables and configuration.

### 6. Testing & Validation
- [ ] Write unit tests for both Flask apps.
- [ ] Test end-to-end flow: web app fetching from the service via Nginx.
- [ ] Add README with setup and usage instructions.

---

**Optional Enhancements**
- Add authentication (JWT or session-based).
- Add persistent storage (e.g., SQLite, PostgreSQL).
- Add frontend interactivity (JavaScript fetch calls, form handling).