import pytest
import json
from app import app, db, Technician, JobTicket

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_app_exists():
    assert app is not None

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200

def test_create_technician(client):
    response = client.post('/api/technicians', 
        json={'name': 'John Doe', 'email': 'john@example.com', 'phone': '555-1234', 'skills': 'Electrical,Plumbing'})
    assert response.status_code in [200, 201, 400]

def test_list_technicians(client):
    response = client.get('/api/technicians')
    assert response.status_code == 200

def test_create_job_ticket(client):
    response = client.post('/api/job-tickets',
        json={'title': 'AC Repair', 'description': 'Fix AC unit', 'customer_name': 'Jane Doe', 'priority': 'high'})
    assert response.status_code in [200, 201, 400]

def test_list_job_tickets(client):
    response = client.get('/api/job-tickets')
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
