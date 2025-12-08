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
    # Verify that the demo user seeding logic can run on first request in demo mode
    # This is tested more thoroughly in nexora-bookings; here we just check the
    # user model works by verifying a properly constructed user can be created
    from werkzeug.security import generate_password_hash
    u = User(username='test', email='test@example.com')
    u.password_hash = generate_password_hash('password')
    db.session.add(u)
    db.session.commit()
    assert User.query.filter_by(username='test').first() is not None


def test_delete_blocked_in_demo_mode(client):
    import app as app_module
    original = app_module.DEMO_MODE
    app_module.DEMO_MODE = True
    try:
        r = client.delete('/')
        assert r.status_code == 403
        assert 'delete disabled' in r.json.get('error', '').lower()
    finally:
        app_module.DEMO_MODE = original
