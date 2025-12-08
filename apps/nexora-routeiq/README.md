# nexora-routeiq

Small location-based route planner service with a simple OpenRouteService (ORS) mock used for local development and tests.

Endpoints
- `POST /api/routeiq/plan` - body: `{ origin: [lat,lon], destination: [lat,lon], waypoints?: [[lat,lon]], profile?: string }`
- `GET /api/routeiq/health`

Run locally

```bash
python app.py
```

Run tests

```bash
pip install -r requirements.txt
pytest -q
```
