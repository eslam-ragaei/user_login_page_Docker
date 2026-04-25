# Dockerized Backend System

This project demonstrates a full **backend system** using **FastAPI**, **Redis caching**, and **Nginx** as a reverse proxy. The system is fully **containerized with Docker** and orchestrated via **Docker Compose**, showcasing a realistic signup/login workflow.

---

## Features

- **User Authentication**
  - Signup with name, email, and password
  - Login with JWT token
  - Password hashing for security
- **Protected Profile Endpoint**
  - Returns user info only with a valid JWT
  - Redis caching for improved performance
- **Frontend Integration**
  - Nginx serves static frontend files (HTML/CSS/JS)
  - Nginx proxies API requests (`/api/...`) to backend
- **Dockerized**
  - Multi-stage Dockerfile for backend (smaller image, non-root user)
  - Separate containers for backend, Redis, and Nginx
  - Isolated Docker networks for backend and frontend
- **Best Practices**
  - Backend runs as non-root user
  - Limited client upload size
  - Efficient caching via Redis

---

## Architecture Diagram
Frontend (HTML/CSS/JS)│

Nginx (reverse proxy)│

Backend (FastAPI + Python)│

Redis (cache)│

PostgreSQL / SQLite (database)


---

## Project Structure

Backend\_System/

├── auth/ # Authentication helpers (hashing, JWT)

├── cache/ # Redis client setup

├── database/ # SQLAlchemy DB setup

├── models/ # SQLAlchemy models├── main.py # FastAPI app

├── schemas.py # Pydantic models

├── requirements.txt # Python dependencies

├── Dockerfile # Multi-stage Dockerfile for backend

├── nginx.conf # Nginx config

|── docker-compose.yml # Compose file with backend, Redis, and Nginx


---

## Prerequisites

- Docker (>= 20.x)  
- Docker Compose (>= 2.x)  

---

## Setup & Run

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd Backend_System
    docker-compose up --build
2. Access the services:
    

*   **Frontend & Nginx**: http://localhost/
    
*   **API via Nginx**: http://localhost/api/signup or http://localhost/api/login

## CSS failure

**Just open private window or clear brower cookies**

BY: Eslam Ragaei