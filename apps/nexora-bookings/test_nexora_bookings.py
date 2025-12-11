import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from app import app, db, User, Module, Calendar, TimeSlot, Appointment
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# ==================== Auth Tests ====================

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

# ==================== Module Management Tests ====================

def test_create_module(client):
    # First create a user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/bookings/modules', json={
        'name': 'Test Module',
        'description': 'Test Description',
        'status': 'active'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Test Module'

def test_list_modules(client):
    client.post('/api/bookings/modules', json={
        'name': 'Module 1',
        'description': 'Desc 1'
    })
    
    response = client.get('/api/bookings/modules')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_module(client):
    create_response = client.post('/api/bookings/modules', json={
        'name': 'Test Module',
        'description': 'Test'
    })
    module_id = create_response.json['id']
    
    response = client.get(f'/api/bookings/modules/{module_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Module'

def test_update_module(client):
    create_response = client.post('/api/bookings/modules', json={
        'name': 'Old Name',
        'description': 'Old Desc'
    })
    module_id = create_response.json['id']
    
    response = client.put(f'/api/bookings/modules/{module_id}', json={
        'name': 'New Name',
        'status': 'inactive'
    })
    assert response.status_code == 200
    assert response.json['name'] == 'New Name'

def test_delete_module(client):
    create_response = client.post('/api/bookings/modules', json={
        'name': 'Test Module'
    })
    module_id = create_response.json['id']
    
    response = client.delete(f'/api/bookings/modules/{module_id}')
    assert response.status_code == 200

# ==================== Calendar Tests ====================

def test_create_calendar(client):
    response = client.post('/api/bookings/calendars', json={
        'name': 'My Calendar',
        'description': 'Test Calendar',
        'timezone': 'America/New_York'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'My Calendar'
    assert response.json['timezone'] == 'America/New_York'

def test_list_calendars(client):
    client.post('/api/bookings/calendars', json={
        'name': 'Calendar 1'
    })
    client.post('/api/bookings/calendars', json={
        'name': 'Calendar 2'
    })
    
    response = client.get('/api/bookings/calendars')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_calendar(client):
    create_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = create_response.json['id']
    
    response = client.get(f'/api/bookings/calendars/{cal_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Calendar'

# ==================== Time Slot Tests ====================

def test_create_time_slot(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    response = client.post(f'/api/bookings/calendars/{cal_id}/time-slots', json={
        'day_of_week': 1,
        'start_time': '09:00',
        'end_time': '17:00',
        'is_available': True
    })
    assert response.status_code == 201
    assert response.json['day_of_week'] == 1
    assert response.json['start_time'] == '09:00'

def test_list_time_slots(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    client.post(f'/api/bookings/calendars/{cal_id}/time-slots', json={
        'day_of_week': 1,
        'start_time': '09:00',
        'end_time': '17:00'
    })
    
    response = client.get(f'/api/bookings/calendars/{cal_id}/time-slots')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_time_slot(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    slot_response = client.post(f'/api/bookings/calendars/{cal_id}/time-slots', json={
        'day_of_week': 1,
        'start_time': '09:00',
        'end_time': '17:00',
        'is_available': True
    })
    slot_id = slot_response.json['id']
    
    response = client.put(f'/api/bookings/time-slots/{slot_id}', json={
        'is_available': False
    })
    assert response.status_code == 200
    assert response.json['is_available'] == False

# ==================== Appointment Tests ====================

def test_create_appointment(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    response = client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Test Appointment',
        'client_name': 'John Doe',
        'client_email': 'john@example.com',
        'client_phone': '123-456-7890',
        'start_time': start.isoformat(),
        'end_time': end.isoformat(),
        'location': 'Conference Room A',
        'description': 'Test appointment'
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Test Appointment'
    assert response.json['status'] == 'pending'

def test_list_appointments(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Appointment 1',
        'start_time': start.isoformat(),
        'end_time': end.isoformat()
    })
    
    response = client.get(f'/api/bookings/appointments?calendar_id={cal_id}')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_appointment(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    apt_response = client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Test Appointment',
        'start_time': start.isoformat(),
        'end_time': end.isoformat()
    })
    apt_id = apt_response.json['id']
    
    response = client.get(f'/api/bookings/appointments/{apt_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Appointment'

def test_update_appointment(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    apt_response = client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Original Title',
        'start_time': start.isoformat(),
        'end_time': end.isoformat()
    })
    apt_id = apt_response.json['id']
    
    response = client.put(f'/api/bookings/appointments/{apt_id}', json={
        'title': 'Updated Title',
        'status': 'confirmed'
    })
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'
    assert response.json['status'] == 'confirmed'

def test_delete_appointment(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    apt_response = client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Test Appointment',
        'start_time': start.isoformat(),
        'end_time': end.isoformat()
    })
    apt_id = apt_response.json['id']
    
    response = client.delete(f'/api/bookings/appointments/{apt_id}')
    assert response.status_code == 200

def test_filter_appointments_by_status(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)
    
    client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Pending Appointment',
        'start_time': start.isoformat(),
        'end_time': end.isoformat(),
        'status': 'pending'
    })
    
    response = client.get(f'/api/bookings/appointments?status=pending')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert all(apt['status'] == 'pending' for apt in response.json)

def test_check_availability(client):
    cal_response = client.post('/api/bookings/calendars', json={
        'name': 'Test Calendar'
    })
    cal_id = cal_response.json['id']
    
    client.post(f'/api/bookings/calendars/{cal_id}/time-slots', json={
        'day_of_week': 1,
        'start_time': '09:00',
        'end_time': '17:00',
        'is_available': True
    })
    
    response = client.get(f'/api/bookings/calendars/{cal_id}/availability')
    assert response.status_code == 200
    assert 'available_slots' in response.json


def test_delete_blocked_in_demo_mode(client):
    # create calendar and appointment
    cal_response = client.post('/api/bookings/calendars', json={'name': 'Demo Calendar'})
    cal_id = cal_response.json['id']

    now = datetime.utcnow()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)

    apt_response = client.post('/api/bookings/appointments', json={
        'calendar_id': cal_id,
        'title': 'Demo Blocked Delete',
        'start_time': start.isoformat(),
        'end_time': end.isoformat()
    })
    apt_id = apt_response.json['id']

    # enable demo mode at runtime and attempt delete
    import app as app_module
    original = app_module.DEMO_MODE
    app_module.DEMO_MODE = True
    try:
        r = client.delete(f'/api/bookings/appointments/{apt_id}')
        assert r.status_code == 403
        assert 'delete disabled' in r.json.get('error', '').lower()
    finally:
        app_module.DEMO_MODE = original

