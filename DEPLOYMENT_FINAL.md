Deployment Checklist — Nexora Suite

This document describes recommended steps to deploy the unified `nexora-home` application in production.

1. Prerequisites
- Linux server (Ubuntu 22.04+ recommended) or container host
- Python 3.11+ and virtualenv
- PostgreSQL production database (recommended) or managed DB
- Domain name and TLS cert (Let’s Encrypt recommended)

2. Environment variables
Set the following in your environment or process manager (do NOT commit to git):
- NEXORA_HOME_SECRET: Flask `SECRET_KEY` (random, 32+ bytes)
- JWT_SECRET: JWT signing secret
- DATABASE_URL: PostgreSQL URI, e.g. `postgresql://user:pass@host:5432/nexora`
- DEMO_MODE: `0` for production
- PORT: optional; Gunicorn will override

3. Install and dependencies
- Create venv: `python -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r requirements.txt`
- Build frontends (if hosting static from server): navigate into each `apps/<module>/frontend` and run the build command (`npm ci && npm run build` or as documented in each module).
- Copy/move built assets into module `frontend/dist` directories if needed.

4. WSGI entrypoint
- The WSGI app is `apps.nexora-home.app:app` (module `apps/nexora-home/app.py`, object `app`).
- With Gunicorn: `gunicorn -w 4 -b 0.0.0.0:8000 apps.nexora-home.app:app`
- Use a process manager (systemd, supervisord) for reliability.

5. Example systemd unit
Create `/etc/systemd/system/nexora.service`:

[Unit]
Description=Nexora Suite
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/nexora-suite
Environment=DATABASE_URL=postgresql://user:pass@host:5432/nexora
Environment=NEXORA_HOME_SECRET=<your-secret>
Environment=JWT_SECRET=<your-jwt-secret>
ExecStart=/srv/nexora-suite/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 apps.nexora-home.app:app
Restart=always

[Install]
WantedBy=multi-user.target

6. Reverse proxy and TLS
- Put Nginx in front, proxy_pass to Gunicorn (127.0.0.1:8000).
- Configure TLS via Certbot or managed cert provider.
- Add security headers, HSTS, and rate limiting as required.

7. Database migrations
- For SQLite: create file-based DB and run the app once to create schema.
- For PostgreSQL/production: integrate Alembic or migration tooling if you change models; currently app uses SQLAlchemy `create_all()` for dev but use migrations for production.

8. Logging & monitoring
- Configure Gunicorn logging to files and rotate logs.
- Add health checks (Nginx endpoint to /api/health or a dedicated /health endpoint).
- Add basic process monitoring (systemd, Prometheus exporter, Sentry for errors).

9. Backups & rollback
- Backup DB daily; test restoration.
- Tag releases and keep a rollback plan (previous release + DB snapshot).

10. Static assets and CDN
- Serve front-end static assets via CDN or Nginx for performance.
- Ensure assets are built with proper publicPath if served under `/module/<name>/`.

11. Security hardening
- Use strong random `NEXORA_HOME_SECRET` and `JWT_SECRET`.
- Set `DEMO_MODE=0`.
- Enforce HTTPS and secure cookies (`SESSION_COOKIE_SECURE = True`).

12. Final smoke tests
- Register -> Login -> Dashboard -> Open several modules, verify API flows and static pages.
- Verify health endpoints for each module.

Notes
- If you deploy on PythonAnywhere, use their WSGI configuration and set environment variables on their web app dashboard.
- Consider containerizing with Docker and Kubernetes for scaling.
