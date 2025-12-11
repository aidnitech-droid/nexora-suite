from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2
import os
import sys

# Add parent directory to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
COMMON_DIR = os.path.abspath(os.path.join(APPS_DIR, '..', 'common'))
sys.path.insert(0, COMMON_DIR)

from utils.pricing_guard import (
    get_pricing_status,
    apply_pricing_middleware,
    is_free_tier_active,
)

app = Flask(__name__)

# Apply pricing middleware
apply_pricing_middleware(app)

DEMO_MODE = os.getenv('DEMO_MODE', '0').lower() in ('1', 'true', 'yes')


@app.before_request
def block_deletes_routeiq():
    from flask import request
    if DEMO_MODE and request.method == 'DELETE':
        return jsonify({'error': 'DELETE disabled in demo mode'}), 403


def haversine(coord1, coord2):
    # coord = (lat, lon) in degrees
    R = 6371.0  # km
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


class MockORSClient:
    """A tiny mock of OpenRouteService routing for unit tests and local dev.

    It returns a straight-line route (LineString) with estimated distance/time
    using simplistic average speeds per profile.
    """

    SPEEDS = {
        'driving-car': 60.0,  # km/h
        'cycling-regular': 18.0,
        'foot-walking': 5.0
    }

    @classmethod
    def plan_route(cls, coords, profile='driving-car'):
        # coords: list of [lat, lon]
        if len(coords) < 2:
            raise ValueError('need at least origin and destination')

        total_km = 0.0
        segments = []
        for a, b in zip(coords[:-1], coords[1:]):
            d = haversine(tuple(a), tuple(b))
            segments.append({'from': a, 'to': b, 'distance_km': d})
            total_km += d

        speed_kmh = cls.SPEEDS.get(profile, cls.SPEEDS['driving-car'])
        # duration in minutes
        duration_min = (total_km / speed_kmh) * 60 if speed_kmh > 0 else None

        # Build a simple LineString
        geometry = {
            'type': 'LineString',
            'coordinates': [[c[1], c[0]] for c in coords]  # lon, lat
        }

        return {
            'geometry': geometry,
            'distance_km': round(total_km, 3),
            'duration_min': round(duration_min, 1) if duration_min is not None else None,
            'profile': profile,
            'segments': segments
        }


# ==================== Module Root ====================

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'module': 'nexora-routeiq',
        'status': 'running',
        'endpoints': ['/api/routeiq/plan', '/api/routeiq/health']
    }), 200


@app.route('/api/routeiq/plan', methods=['POST'])
def plan():
    """Plan a route given origin, destination, optional waypoints and profile.

    Request JSON:
      {
        "origin": [lat, lon],
        "destination": [lat, lon],
        "waypoints": [[lat, lon], ...],  # optional
        "profile": "driving-car"  # optional
      }

    Returns a simplified ORS-like response with geometry, distance and duration.
    """
    data = request.get_json() or {}
    origin = data.get('origin')
    destination = data.get('destination')
    waypoints = data.get('waypoints', []) or []
    profile = data.get('profile', 'driving-car')

    if not origin or not destination:
        return jsonify({'error': 'origin and destination required'}), 400

    try:
        coords = [origin] + waypoints + [destination]
        route = MockORSClient.plan_route(coords, profile=profile)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'route': route}), 200


@app.route('/api/routeiq/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'nexora-routeiq'}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5050'))
    app.run(host='0.0.0.0', port=port)
