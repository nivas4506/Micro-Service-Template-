# MicroDeploy — Microservices CI/CD Pipeline & Platform

A modern microservices platform built with FastAPI, Docker Compose, Kubernetes, and GitHub Actions. MicroDeploy demonstrates an end-to-end cloud-native architecture featuring an API gateway, domain microservices, a lightweight frontend, and automated testing and CI/CD workflows.

---

## 📑 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Service Catalog](#-service-catalog)
- [Project Structure](#-project-structure)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Quickstart (Local Development)](#-quickstart-local-development)
  - [Prerequisites](#prerequisites)
  - [Using Docker Compose](#using-docker-compose)
  - [Using Local Python Environment](#using-local-python-environment)
- [Endpoints & Verification](#-endpoints--verification)
- [Infrastructure & Deployment](#-infrastructure--deployment)
  - [Kubernetes](#kubernetes)
  - [Monitoring](#monitoring)
- [Testing & Quality](#-testing--quality)
- [Makefile Commands](#-makefile-commands)

---

## 🏛️ Architecture Overview

The system follows a microservices pattern with client traffic routed through a lightweight frontend and aggregated via a centralized API Gateway:

```text
[ Client / Browser ]
        │
        ▼
[ Frontend (Nginx) :3000 ]
        │
        ▼
[ API Gateway (FastAPI) :8000 ]
        │
   ┌────┼──────────────┬──────────────┬────────────────┐
   ▼    ▼              ▼              ▼                ▼
[Users] [Products]    [Orders]       [Payments]       [Notifications]
(:8001) (:8002)       (:8003)        (:8004)          (:8005)
```

---

## 📦 Service Catalog

| Service | Port | Tech Stack | Responsibility |
|---------|------|------------|----------------|
| **Frontend** | `3000` | Nginx, HTML5 | Dashboard UI & status client |
| **API Gateway** | `8000` | FastAPI, HTTPX | Central routing, service discovery & health aggregation |
| **User Service** | `8001` | FastAPI, Uvicorn | User account management & profile data |
| **Product Service** | `8002` | FastAPI, Uvicorn | Product catalog & inventory details |
| **Order Service** | `8003` | FastAPI, Uvicorn | Order creation & lifecycle handling |
| **Payment Service** | `8004` | FastAPI, Uvicorn | Payment processing mock / transactions |
| **Notification Service** | `8005` | FastAPI, Uvicorn | Alerts and event notifications |

---

## 📂 Project Structure

```text
Pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI workflow (lint, test, build)
├── docs/
│   └── architecture.md            # Architecture reference notes
├── frontend/
│   ├── Dockerfile                 # Nginx container definition
│   ├── nginx.conf                 # Reverse proxy configuration
│   └── index.html                 # Simple status and service dashboard UI
├── gateway/
│   ├── Dockerfile                 # Gateway container
│   ├── app.py                     # FastAPI gateway aggregator & router
│   └── requirements.txt           # Gateway dependencies
├── infrastructure/
│   ├── docker/                    # Auxiliary compose setups (e.g. monitoring)
│   ├── helm/                      # Helm deployment charts
│   ├── kubernetes/                # Kubernetes manifests (deployments & services)
│   └── monitoring/                # Prometheus / Grafana configurations
├── services/
│   ├── user-service/              # User domain service
│   ├── product-service/           # Product domain service
│   ├── order-service/             # Order domain service
│   ├── payment-service/           # Payment domain service
│   └── notification-service/      # Notification domain service
├── tests/
│   ├── conftest.py                # Pytest fixtures and mock client setup
│   ├── test_gateway.py            # Gateway unit/integration tests
│   └── test_services.py           # Microservices endpoint test suite
├── docker-compose.yml             # Local multi-service orchestration
├── Makefile                       # Convenient developer tasks
├── pytest.ini                     # Pytest configuration
└── requirements.txt               # Top-level dependencies
```

---

## 🚀 CI/CD Pipeline

The project includes an automated GitHub Actions workflow defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) triggered on pushes and pull requests to `main` / `master`.

The pipeline consists of three sequential/dependent stages:

```text
┌──────────────┐      ┌──────────────┐
│  Unit Tests  │      │     Lint     │
│ (pytest -v)  │      │ (ruff check) │
└──────┬───────┘      └──────┬───────┘
       │                     │
       └──────────┬──────────┘
                  ▼
         ┌─────────────────┐
         │  Docker Build   │
         │ (compose build) │
         └─────────────────┘
```

1. **Test Job**:
   - Environment: Ubuntu Latest, Python 3.12
   - Runs `pytest tests/ -v` testing all microservices and gateway proxy endpoints.
2. **Lint Job**:
   - Runs `ruff check services/ gateway/ tests/` for linting and code quality validation.
3. **Build Job**:
   - Depends on `test` and `lint` passing.
   - Executes `docker compose build` to ensure all containers build without errors.

---

## ⚡ Quickstart (Local Development)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Python 3.12+](https://www.python.org/downloads/) (for running tests/linting locally)
- `make` (optional, for CLI shortcuts)

### Using Docker Compose

Start the entire microservices stack with a single command:

```bash
# Using Makefile
make up

# Or directly with Docker Compose
docker compose up --build -d
```

Check the status and container logs:

```bash
docker compose ps
make logs
```

Stop and tear down the environment:

```bash
make down
# Or to remove volumes and local images:
make clean
```

### Using Local Python Environment

If you want to run tests or services without Docker:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest httpx ruff
```

---

## 🔍 Endpoints & Verification

Once services are running, verify them using `curl` or your browser:

### 1. Web UI Dashboard
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 2. API Gateway
- **Gateway Health**:
  ```bash
  curl http://localhost:8000/health
  # {"service":"api-gateway","status":"healthy"}
  ```
- **Aggregated Services Status**:
  ```bash
  curl http://localhost:8000/services
  ```
- **Service Proxies**:
  ```bash
  curl http://localhost:8000/users
  curl http://localhost:8000/products
  curl http://localhost:8000/orders
  ```

---

## ☸️ Infrastructure & Deployment

### Kubernetes

Pre-configured manifests are available under `infrastructure/kubernetes/`:

```bash
kubectl apply -f infrastructure/kubernetes/namespace.yaml
kubectl apply -f infrastructure/kubernetes/user-service.yaml
kubectl apply -f infrastructure/kubernetes/gateway.yaml
```

### Monitoring

Prometheus and Grafana setups are available in `infrastructure/monitoring/` and `infrastructure/docker/` for metrics aggregation and cluster observability.

---

## 🧪 Testing & Quality

Run the test suite and code linter locally:

```bash
# Run pytest unit & integration tests
make test
# Or: pytest tests/ -v

# Run Ruff linter
make lint
# Or: ruff check services/ gateway/ tests/
```

---

## 🛠️ Makefile Commands

| Command | Action |
|---------|--------|
| `make up` | Builds and launches all microservices in the background |
| `make down` | Stops all running microservices |
| `make build` | Builds or rebuilds service container images |
| `make logs` | Streams logs from all running services |
| `make test` | Executes test suite with pytest |
| `make lint` | Installs and runs Ruff linter across services, gateway, and tests |
| `make health` | Queries gateway health and aggregated services endpoints |
| `make clean` | Stops containers and removes local images & volumes |

---

## 📄 License

This repository is maintained for microservice deployment and CI/CD demonstration purposes.
