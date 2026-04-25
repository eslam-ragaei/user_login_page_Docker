# Dockerized Login System

A complete Docker-based authentication demo built with:
- FastAPI backend
- PostgreSQL database
- Redis cache
- Nginx reverse proxy / static frontend server
- Docker Compose orchestration

This repository combines a simple signup/login API with a static frontend served through Nginx and a backend service that caches user profile data in Redis.

---

## What this project includes

- FastAPI backend with endpoints for:
  - `POST /api/signup` — create a new user
  - `POST /api/login` — authenticate a user
  - `GET /api/profile` — return user data for an authenticated request
- PostgreSQL container for persistent user storage
- Redis container for caching profile responses
- Nginx container serving the frontend and proxying `/api/` requests to FastAPI
- Multi-stage Docker build for a smaller backend image

---

## Architecture

- `frontend/` contains static HTML, CSS, and JavaScript
- `nginx/nginx.conf` serves `/` from the static frontend and proxies `/api/` requests to the backend
- `backend/` contains the FastAPI application and a Dockerfile
- `docker-compose.yml` wires together `backend`, `db`, `redis`, and `nginx`

---

## Hosted services

- Frontend + Nginx: `http://localhost/`
- API through Nginx: `http://localhost/api/`
- Direct backend port: `http://localhost:8000/`

---

## Environment variables

Create a `.env` file in the project root with values such as:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
SECRET_KEY=supersecretkey
```

The backend uses `DATABASE_URL` if set, otherwise it defaults to:

```text
postgresql://user:password@db:5432/mydatabase
```

---

## Run locally

From the repository root:

```bash
docker-compose up --build
```

Then open:

```text
http://localhost/
```

---

## API endpoints

### Signup

`POST /api/signup`

Request JSON:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

Returns a success message when registration succeeds.

### Login

`POST /api/login`

Request JSON:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

The backend generates a JWT token internally.

### Profile

`GET /api/profile`

Requires the `Authorization` header:

```text
Authorization: Bearer <JWT_TOKEN>
```

Returns cached profile data from Redis when available, or loads it from PostgreSQL and caches it.

---

## Project structure

```text
.
├── backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app
│       ├── auth.py
│       ├── cache.py
│       ├── database.py
│       ├── main.py
│       ├── schemas.py
│       └── user_models.py
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── nginx
│   └── nginx.conf
└── docker-compose.yml
```

---

## Notes

- Nginx serves the static frontend from `frontend/`
- `/api/` calls are proxied to the backend service on port `8000`
- Redis caches profile responses for one hour
- The backend runs as a non-root user inside the container

---

## Troubleshooting

- If the browser shows stale behavior, clear the browser cache or use a private/incognito window.
- Ensure Docker and Docker Compose are installed and running.
- If PostgreSQL connection issues occur, verify `.env` values and restart the compose stack.

