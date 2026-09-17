# Architecture

MicroDeploy is a microservices platform with five domain services behind a single API gateway.

## Services

| Service | Port | Responsibility |
|---------|------|----------------|
| user-service | 8001 | User management |
| product-service | 8002 | Product catalog |
| order-service | 8003 | Order processing |
| payment-service | 8004 | Payment handling |
| notification-service | 8005 | Notifications |
| gateway | 8000 | API aggregation |
| frontend | 3000 | Web UI |

## Request Flow

```
Client → Frontend (nginx) → Gateway → Service
```

The gateway proxies requests to backend services and exposes a `/services` endpoint for health aggregation.

## Deployment Options

- **Local**: `make up` (Docker Compose)
- **Kubernetes**: manifests in `infrastructure/kubernetes/`
- **Helm**: chart in `infrastructure/helm/`
- **Monitoring**: Prometheus + Grafana via `infrastructure/docker/docker-compose.monitoring.yml`
