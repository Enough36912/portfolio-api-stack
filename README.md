# Portfolio API Stack (FastAPI + Postgres + Prometheus Metrics)

A Dockerized FastAPI service with Postgres persistence, a simple visit counter, health checks, and a `/metrics` endpoint for Prometheus-style observability.

## Quick start
```bash
docker compose up -d --build
```

## Endpoints
- `GET /` (service info)
- `GET /health` (db health)
- `GET /visits` (current count)
- `POST /visits/increment` (increment count)
- `GET /metrics` (Prometheus metrics)

## Local URLs
- Swagger UI: http://localhost:8080/docs
- Metrics: http://localhost:8080/metrics
