# Portfolio API Stack (Docker + FastAPI + Postgres)
Run a production-style local stack with 1 command.

## Run
docker compose up -d --build

## Test
- Health:  http://localhost:8080/health
- Visits:  http://localhost:8080/visits
- Inc:     POST http://localhost:8080/visits/increment

## Docs (Swagger UI)
http://localhost:8080/docs

## Stop
docker compose down
