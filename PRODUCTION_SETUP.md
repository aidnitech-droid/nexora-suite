# Production Deployment Setup

This directory contains configuration files and scripts for deploying Nexora Suite in production.

## Files

- `Dockerfile` — Multi-stage Docker image for Nexora (Python 3.12-slim, gunicorn)
- `docker-compose.yml` — Production-ready compose stack with PostgreSQL, Redis, Nginx, and Nexora
- `nexora.service` — Systemd service unit for auto-start and process management
- `nginx.conf` — Nginx reverse proxy configuration with security headers and caching
- `DEPLOYMENT_FINAL.md` — Full deployment guide (env vars, migrations, WSGI config)
- `LAUNCH_CHECKLIST.md` — Pre/post-launch checklist
- `tests/e2e_nexora.py` — End-to-end tests using Playwright (user flows: register → login → dashboard → modules)

## Quick Start (Docker Compose)

```bash
# 1. Set up environment variables
cp .env.example .env
# Edit .env with your NEXORA_HOME_SECRET, JWT_SECRET, and DB password

# 2. Build and start services
docker-compose up -d

# 3. Run migrations (if using Alembic/Alembic)
docker-compose exec nexora-home alembic upgrade head

# 4. Verify health
curl http://localhost:8000/
```

## Systemd Setup (Bare Metal)

```bash
# 1. Clone repo to /srv/nexora-suite
cd /srv/nexora-suite

# 2. Create venv and install
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt gunicorn

# 3. Create nexora user (if not exists)
sudo useradd -m -s /bin/bash nexora

# 4. Set ownership
sudo chown -R nexora:nexora /srv/nexora-suite

# 5. Install systemd service
sudo cp nexora.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nexora
sudo systemctl start nexora

# 6. Check status
sudo systemctl status nexora
```

## E2E Testing

```bash
# Install playwright browsers
python -m playwright install chromium

# Run E2E tests (requires app running on http://localhost:5060)
pytest tests/e2e_nexora.py -v
```

## Nginx Setup

1. Update `nginx.conf` with your domain name.
2. Configure SSL certificates (Let's Encrypt recommended).
3. Copy to Nginx config directory:
   ```bash
   sudo cp nginx.conf /etc/nginx/nginx.conf
   sudo systemctl reload nginx
   ```

## Security Checklist

- [ ] Change `NEXORA_HOME_SECRET` and `JWT_SECRET` to random 32+ byte strings
- [ ] Change PostgreSQL password in docker-compose and environment
- [ ] Enable TLS/HTTPS with valid certificate
- [ ] Set up firewall rules (allow 80, 443, restrict DB port)
- [ ] Configure log rotation
- [ ] Set up monitoring and alerting
- [ ] Regular backups of PostgreSQL data
