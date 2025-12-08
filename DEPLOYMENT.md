# Deployment notes

This document contains quick steps to deploy the core services locally or to a container platform.

Local with Docker Compose

1. Build and run the stack (demo mode enabled by default):

```bash
export DEMO_MODE=true
docker-compose up --build
```

Services:
- `nexora-home` — http://localhost:5060
- `nexora-bookings` — http://localhost:5000
- `nexora-routeiq` — http://localhost:5050

Notes for production
- Replace SQLite with a managed DB (Postgres) and configure `DATABASE_URL`.
- Configure a proper secret for `NEXORA_HOME_SECRET` and JWT secrets for other services.
- Add TLS via a reverse proxy (Traefik, Nginx) and secure service-to-service comms.
