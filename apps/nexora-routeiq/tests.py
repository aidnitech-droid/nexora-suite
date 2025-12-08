import json
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get('/api/routeiq/health')
    assert r.status_code == 200
    assert r.json['service'] == 'nexora-routeiq'


def test_plan_route_minimal(client):
    body = {
        'origin': [40.7128, -74.0060],  # NYC
        'destination': [40.730610, -73.935242],  # Brooklyn-ish
    }
    r = client.post('/api/routeiq/plan', json=body)
    assert r.status_code == 200
    route = r.json['route']
    assert 'geometry' in route
    assert route['distance_km'] > 0
    assert route['duration_min'] > 0


def test_plan_route_with_waypoints_and_profile(client):
    body = {
        'origin': [40.7128, -74.0060],
        'waypoints': [[40.7200, -73.9950]],
        'destination': [40.730610, -73.935242],
        'profile': 'foot-walking'
    }
    r = client.post('/api/routeiq/plan', json=body)
    assert r.status_code == 200
    route = r.json['route']
    assert route['profile'] == 'foot-walking'
    assert len(route['geometry']['coordinates']) == 3


def test_plan_route_errors(client):
    # missing fields
    r = client.post('/api/routeiq/plan', json={})
    assert r.status_code == 400


def test_delete_blocked_in_demo_mode(client):
    # The app's before_request should block DELETE when DEMO_MODE is True
    import sys
    from app import app as flask_app
    import app as app_module
    original = app_module.DEMO_MODE
    app_module.DEMO_MODE = True
    try:
        r = client.delete('/api/routeiq/health')
        assert r.status_code == 403
        assert 'delete disabled' in r.json.get('error', '').lower()
    finally:
        app_module.DEMO_MODE = original
