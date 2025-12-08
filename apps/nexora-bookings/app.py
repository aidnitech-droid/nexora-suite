from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta, datetime
import uuid
import json

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
DEMO_MODE = os.getenv('DEMO_MODE', '0').lower() in ('1', 'true', 'yes')
DEMO_CREDENTIALS = {
    'email': 'demo@nexora.com',
    'username': 'demo',
    'password': 'Demo1234',
    'role': 'demo'
}


@app.before_request
def block_deletes_global():
    if DEMO_MODE and request.method == 'DELETE':
        return jsonify({'error': 'DELETE disabled in demo mode'}), 403

# ==================== Models ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Module(db.Model):
    __tablename__ = 'module_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

# ==================== Role-based decorator ====================

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ==================== Auth Endpoints ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'access_token': access_token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or user.password != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'access_token': access_token
    }), 200

# ==================== Module Management Endpoints ====================

@app.route('/api/bookings/modules', methods=['POST'])
def create_module():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    
    user_id = request.args.get('user_id', type=int)
    module = Module(
        title=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active'),
        created_by=user_id
    )
    db.session.add(module)
    db.session.commit()
    
    return jsonify({
        'id': module.id,
        'name': module.title,
        'description': module.description,
        'status': module.status
    }), 201


@app.route('/api/bookings/modules', methods=['GET'])
def list_modules():
    modules = Module.query.order_by(Module.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'name': m.title,
        'description': m.description,
        'status': m.status,
        'created_at': m.created_at.isoformat() if m.created_at else None
    } for m in modules]), 200


@app.route('/api/bookings/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    module = Module.query.get_or_404(module_id)
    return jsonify({
        'id': module.id,
        'name': module.title,
        'description': module.description,
        'status': module.status,
        'created_at': module.created_at.isoformat() if module.created_at else None
    }), 200


@app.route('/api/bookings/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    module = Module.query.get_or_404(module_id)
    data = request.get_json() or {}
    
    if 'name' in data:
        module.title = data['name']
    if 'description' in data:
        module.description = data['description']
    if 'status' in data:
        module.status = data['status']
    
    db.session.commit()
    return jsonify({
        'id': module.id,
        'name': module.title,
        'description': module.description,
        'status': module.status
    }), 200


@app.route('/api/bookings/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({'message': 'Module deleted successfully'}), 200

# ==================== CRUD Endpoints ====================

@app.route('/api/items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    items = Module.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': items.total,
        'pages': items.pages,
        'current_page': page,
        'items': [{
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'status': item.status,
            'created_at': item.created_at
        } for item in items.items]
    }), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status,
        'created_at': item.created_at
    }), 200

@app.route('/api/items', methods=['POST'])
@role_required(['admin', 'manager'])
def create_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    item = Module(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'active'),
        created_by=user_id
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status
    }), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@role_required(['admin', 'manager'])
def update_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.status = data.get('status', item.status)
    
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status
    }), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item deleted successfully'}), 200


# ------------------ Appointment Scheduler & Calendar ------------------

class Calendar(db.Model):
    __tablename__ = 'booking_calendars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)
    timezone = db.Column(db.String(50), default='UTC')
    created_at = db.Column(db.DateTime, default=db.func.now())

    owner = db.relationship('User', backref=db.backref('calendars', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'description': self.description,
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TimeSlot(db.Model):
    __tablename__ = 'booking_time_slots'
    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('booking_calendars.id'))
    day_of_week = db.Column(db.Integer)  # 0-6 (Mon-Sun)
    start_time = db.Column(db.String(5))  # HH:MM format
    end_time = db.Column(db.String(5))  # HH:MM format
    is_available = db.Column(db.Boolean, default=True)

    calendar = db.relationship('Calendar', backref=db.backref('time_slots', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'calendar_id': self.calendar_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'is_available': self.is_available
        }


class Appointment(db.Model):
    __tablename__ = 'booking_appointments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:12])
    calendar_id = db.Column(db.Integer, db.ForeignKey('booking_calendars.id'))
    client_name = db.Column(db.String(255))
    client_email = db.Column(db.String(255))
    client_phone = db.Column(db.String(50))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled, completed
    location = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    calendar = db.relationship('Calendar', backref=db.backref('appointments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'calendar_id': self.calendar_id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'client_phone': self.client_phone,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'location': self.location,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


with app.app_context():
    db.create_all()
    # Seed demo user and example data when running in demo mode
    if DEMO_MODE:
        demo = User.query.filter((User.username == DEMO_CREDENTIALS['username']) | (User.email == DEMO_CREDENTIALS['email'])).first()
        if not demo:
            demo = User(username=DEMO_CREDENTIALS['username'], email=DEMO_CREDENTIALS['email'], password=DEMO_CREDENTIALS['password'], role=DEMO_CREDENTIALS['role'])
            db.session.add(demo)
            db.session.commit()

        # Demo calendar
        cal = Calendar.query.filter_by(name='Demo Calendar').first()
        if not cal:
            cal = Calendar(name='Demo Calendar', owner_id=demo.id, description='Demo calendar for Nexora demo', timezone='UTC')
            db.session.add(cal)
            db.session.commit()

        # Demo time slot
        ts = TimeSlot.query.filter_by(calendar_id=cal.id, day_of_week=1, start_time='09:00').first()
        if not ts:
            ts = TimeSlot(calendar_id=cal.id, day_of_week=1, start_time='09:00', end_time='17:00', is_available=True)
            db.session.add(ts)
            db.session.commit()

        # Demo appointment
        apt = Appointment.query.filter_by(title='Demo Appointment').first()
        if not apt:
            now = datetime.utcnow()
            start = now + timedelta(hours=1)
            end = start + timedelta(hours=1)
            apt = Appointment(calendar_id=cal.id, client_name='Demo User', client_email=demo.email, title='Demo Appointment', start_time=start, end_time=end, status='confirmed', location='Demo Location')
            db.session.add(apt)
            db.session.commit()


# Calendar endpoints
@app.route('/api/bookings/calendars', methods=['POST'])
def create_calendar():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    cal = Calendar(
        name=data['name'],
        owner_id=data.get('owner_id'),
        description=data.get('description'),
        timezone=data.get('timezone', 'UTC')
    )
    db.session.add(cal)
    db.session.commit()
    return jsonify(cal.to_dict()), 201


@app.route('/api/bookings/calendars', methods=['GET'])
def list_calendars():
    calendars = Calendar.query.order_by(Calendar.created_at.desc()).all()
    return jsonify([c.to_dict() for c in calendars]), 200


@app.route('/api/bookings/calendars/<int:cal_id>', methods=['GET'])
def get_calendar(cal_id):
    cal = Calendar.query.get_or_404(cal_id)
    return jsonify(cal.to_dict()), 200


# Time slot endpoints
@app.route('/api/bookings/calendars/<int:cal_id>/time-slots', methods=['POST'])
def create_time_slot(cal_id):
    cal = Calendar.query.get_or_404(cal_id)
    data = request.get_json() or {}
    if 'day_of_week' not in data or not data.get('start_time') or not data.get('end_time'):
        return jsonify({'error': 'day_of_week, start_time, end_time required'}), 400
    slot = TimeSlot(
        calendar_id=cal_id,
        day_of_week=data['day_of_week'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        is_available=data.get('is_available', True)
    )
    db.session.add(slot)
    db.session.commit()
    return jsonify(slot.to_dict()), 201


@app.route('/api/bookings/calendars/<int:cal_id>/time-slots', methods=['GET'])
def list_time_slots(cal_id):
    cal = Calendar.query.get_or_404(cal_id)
    slots = TimeSlot.query.filter(TimeSlot.calendar_id == cal_id).all()
    return jsonify([s.to_dict() for s in slots]), 200


@app.route('/api/bookings/time-slots/<int:slot_id>', methods=['PUT'])
def update_time_slot(slot_id):
    slot = TimeSlot.query.get_or_404(slot_id)
    data = request.get_json() or {}
    if 'is_available' in data:
        slot.is_available = data.get('is_available')
    db.session.commit()
    return jsonify(slot.to_dict()), 200


# Appointment endpoints
@app.route('/api/bookings/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json() or {}
    if not data.get('calendar_id') or not data.get('title') or not data.get('start_time') or not data.get('end_time'):
        return jsonify({'error': 'calendar_id, title, start_time, end_time required'}), 400
    cal = Calendar.query.get_or_404(data['calendar_id'])
    try:
        start = datetime.fromisoformat(data['start_time'])
        end = datetime.fromisoformat(data['end_time'])
    except Exception:
        return jsonify({'error': 'invalid datetime format'}), 400
    apt = Appointment(
        calendar_id=data['calendar_id'],
        client_name=data.get('client_name'),
        client_email=data.get('client_email'),
        client_phone=data.get('client_phone'),
        title=data['title'],
        description=data.get('description'),
        start_time=start,
        end_time=end,
        status=data.get('status', 'pending'),
        location=data.get('location'),
        notes=data.get('notes')
    )
    db.session.add(apt)
    db.session.commit()
    return jsonify(apt.to_dict()), 201


@app.route('/api/bookings/appointments', methods=['GET'])
def list_appointments():
    cal_id = request.args.get('calendar_id', type=int)
    status = request.args.get('status')
    q = Appointment.query
    if cal_id:
        q = q.filter(Appointment.calendar_id == cal_id)
    if status:
        q = q.filter(Appointment.status == status)
    appointments = q.order_by(Appointment.start_time.asc()).all()
    return jsonify([a.to_dict() for a in appointments]), 200


@app.route('/api/bookings/appointments/<int:apt_id>', methods=['GET'])
def get_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    return jsonify(apt.to_dict()), 200


@app.route('/api/bookings/appointments/<int:apt_id>', methods=['PUT'])
def update_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    data = request.get_json() or {}
    apt.client_name = data.get('client_name', apt.client_name)
    apt.client_email = data.get('client_email', apt.client_email)
    apt.client_phone = data.get('client_phone', apt.client_phone)
    apt.title = data.get('title', apt.title)
    apt.description = data.get('description', apt.description)
    apt.location = data.get('location', apt.location)
    apt.notes = data.get('notes', apt.notes)
    if 'status' in data:
        apt.status = data.get('status')
    if data.get('start_time'):
        try:
            apt.start_time = datetime.fromisoformat(data['start_time'])
        except Exception:
            pass
    if data.get('end_time'):
        try:
            apt.end_time = datetime.fromisoformat(data['end_time'])
        except Exception:
            pass
    db.session.commit()
    return jsonify(apt.to_dict()), 200


@app.route('/api/bookings/appointments/<int:apt_id>', methods=['DELETE'])
def delete_appointment(apt_id):
    if DEMO_MODE:
        return jsonify({'error': 'delete disabled in demo mode'}), 403
    apt = Appointment.query.get_or_404(apt_id)
    db.session.delete(apt)
    db.session.commit()
    return jsonify({'message': 'appointment deleted'}), 200


# Availability check endpoint
@app.route('/api/bookings/calendars/<int:cal_id>/availability', methods=['GET'])
def check_availability(cal_id):
    cal = Calendar.query.get_or_404(cal_id)
    # Simple check: return available time slots for the calendar
    slots = TimeSlot.query.filter(TimeSlot.calendar_id == cal_id, TimeSlot.is_available == True).all()
    return jsonify({'calendar_id': cal_id, 'available_slots': [s.to_dict() for s in slots]}), 200


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-bookings'}), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
