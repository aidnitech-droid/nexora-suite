# API documentation (OpenAPI)

This folder contains an aggregated OpenAPI 3.0 specification for the Nexora Suite micro-apps and a small Redoc index to view it locally.

Files
- `openapi.yaml` — OpenAPI 3 definition covering main endpoints across apps (bookings, routeiq, home).
- `index.html` — Redoc viewer; opens `openapi.yaml`.

View locally

1. From the `docs/` directory run a simple HTTP server:

```bash
cd docs
python -m http.server 8000
# then open http://localhost:8000/index.html in your browser
```

Notes
- This spec is a consolidated starting point and documents the main routes discovered in the codebase. For production use you may want to:
  - Keep the spec in-sync with code (automate with tests/CI or use docstrings/openapi decorators).
  - Add security schemes for JWT/session auth and required request/response examples.

Demo Mode
- Set `DEMO_MODE=true` in your environment to enable demo mode across apps. Demo mode:
  - Seeds a demo user: `demo@nexora.com` / `Demo1234`.
  - Disables destructive HTTP verbs (DELETE).
  - Seeds sample data for `nexora-bookings` (calendar, time slot, appointment).

To try demo mode locally:

```bash
export DEMO_MODE=true
# run the app(s), e.g.:
python apps/nexora-home/app.py
python apps/nexora-bookings/app.py
```
