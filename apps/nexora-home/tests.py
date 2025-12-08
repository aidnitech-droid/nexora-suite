import pytest

from app import app, db, User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_index_accessible(client):
    r = client.get('/')
    assert r.status_code in (200, 302)  # may redirect for login


def test_demo_user_seeded_when_demo_mode(client):
    # Ensure demo user is created when DEMO_MODE is True
    original = app.DEMO_MODE
    app.DEMO_MODE = True
    try:
        # trigger before_first_request handler
        with app.test_client() as c:
            c.get('/')
        demo = User.query.filter_by(email='demo@nexora.com').first()
        assert demo is not None
        assert demo.username == 'demo'
    finally:
        app.DEMO_MODE = original


def test_delete_blocked_in_demo_mode(client):
    original = app.DEMO_MODE
    app.DEMO_MODE = True
    try:
        r = client.delete('/')
        assert r.status_code == 403
        assert 'delete disabled' in r.json.get('error', '').lower()
    finally:
        app.DEMO_MODE = original
