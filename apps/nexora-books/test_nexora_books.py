import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from app import app, db, User, Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'

def test_login(client):
    # Register first
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_create_book(client):
    # Register and login
    reg = client.post('/api/auth/register', json={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password123',
        'role': 'admin'
    })
    token = reg.json['access_token']
    
    # Create book
    response = client.post('/api/books', 
        json={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '123-456-789',
            'price': 29.99,
            'stock': 10
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Test Book'

def test_get_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    assert 'books' in response.json

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
