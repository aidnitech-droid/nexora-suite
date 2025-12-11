from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta

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

# ==================== Module Root ====================

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'module': 'nexora-assist',
        'status': 'running',
        'endpoints': ['/api/auth/register', '/api/auth/login', '/api/items', '/api/health']
    }), 200

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

# ------------------ Remote Support Request & Session Logs ------------------

class SupportRequest(db.Model):
    __tablename__ = 'assist_support_requests'
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:12])
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    customer_name = db.Column(db.String(255))
    customer_contact = db.Column(db.String(255))
    severity = db.Column(db.String(20), default='normal')  # low, normal, high, critical
    status = db.Column(db.String(50), default='open')  # open, in_progress, resolved, closed
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    preferred_time = db.Column(db.DateTime, nullable=True)
    meta_info = db.Column(db.Text)  # JSON blob for extra info
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        meta = None
        try:
            meta = json.loads(self.meta_info) if self.meta_info else None
        except Exception:
            meta = None
        return {
            'id': self.id,
            'request_number': self.request_number,
            'subject': self.subject,
            'description': self.description,
            'customer_name': self.customer_name,
            'customer_contact': self.customer_contact,
            'severity': self.severity,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'preferred_time': self.preferred_time.isoformat() if self.preferred_time else None,
            'metadata': meta,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SessionLog(db.Model):
    __tablename__ = 'assist_session_logs'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('assist_support_requests.id'))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    entry_type = db.Column(db.String(50), default='note')  # note, system, event
    message = db.Column(db.Text)
    meta_info = db.Column(db.Text)

    request = db.relationship('SupportRequest', backref=db.backref('session_logs', lazy=True))

    def to_dict(self):
        meta = None
        try:
            meta = json.loads(self.meta_info) if self.meta_info else None
        except Exception:
            meta = None
        return {
            'id': self.id,
            'request_id': self.request_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'actor_id': self.actor_id,
            'entry_type': self.entry_type,
            'message': self.message,
            'metadata': meta
        }


with app.app_context():
    db.create_all()


# Support request endpoints
@app.route('/api/assist/requests', methods=['POST'])
def create_support_request():
    data = request.get_json() or {}
    if not data.get('subject'):
        return jsonify({'error': 'subject required'}), 400
    pref = None
    if data.get('preferred_time'):
        try:
            pref = datetime.fromisoformat(data.get('preferred_time'))
        except Exception:
            pref = None
    metadata = None
    if data.get('metadata'):
        try:
            metadata = json.dumps(data.get('metadata'))
        except Exception:
            metadata = None
    req = SupportRequest(
        subject=data['subject'],
        description=data.get('description'),
        customer_name=data.get('customer_name'),
        customer_contact=data.get('customer_contact'),
        severity=data.get('severity', 'normal'),
        preferred_time=pref,
        metadata=metadata
    )
    db.session.add(req)
    db.session.commit()
    return jsonify(req.to_dict()), 201


@app.route('/api/assist/requests', methods=['GET'])
def list_support_requests():
    status = request.args.get('status')
    assigned = request.args.get('assigned_to', type=int)
    q = SupportRequest.query
    if status:
        q = q.filter(SupportRequest.status == status)
    if assigned:
        q = q.filter(SupportRequest.assigned_to == assigned)
    items = q.order_by(SupportRequest.created_at.desc()).all()
    return jsonify([r.to_dict() for r in items]), 200


@app.route('/api/assist/requests/<int:request_id>', methods=['GET'])
def get_support_request(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    return jsonify(r.to_dict()), 200


@app.route('/api/assist/requests/<int:request_id>', methods=['PUT'])
def update_support_request(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    data = request.get_json() or {}
    r.subject = data.get('subject', r.subject)
    r.description = data.get('description', r.description)
    r.customer_name = data.get('customer_name', r.customer_name)
    r.customer_contact = data.get('customer_contact', r.customer_contact)
    r.severity = data.get('severity', r.severity)
    if data.get('preferred_time'):
        try:
            r.preferred_time = datetime.fromisoformat(data.get('preferred_time'))
        except Exception:
            pass
    if 'status' in data:
        r.status = data.get('status')
    if 'assigned_to' in data:
        r.assigned_to = data.get('assigned_to')
    if 'metadata' in data:
        try:
            r.metadata = json.dumps(data.get('metadata'))
        except Exception:
            pass
    db.session.commit()
    return jsonify(r.to_dict()), 200


@app.route('/api/assist/requests/<int:request_id>', methods=['DELETE'])
def delete_support_request(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    # delete logs first
    for log in r.session_logs:
        db.session.delete(log)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'request deleted'}), 200


# Session logs endpoints
@app.route('/api/assist/requests/<int:request_id>/session/start', methods=['POST'])
def start_session(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    data = request.get_json() or {}
    # create an initial session log entry
    entry = SessionLog(request_id=r.id, actor_id=data.get('actor_id'), entry_type='system', message=data.get('message','session started'), metadata=json.dumps(data.get('metadata') or {}))
    r.status = 'in_progress'
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201


@app.route('/api/assist/requests/<int:request_id>/session/logs', methods=['GET'])
def get_session_logs(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    logs = SessionLog.query.filter(SessionLog.request_id == r.id).order_by(SessionLog.timestamp.asc()).all()
    return jsonify([l.to_dict() for l in logs]), 200


@app.route('/api/assist/requests/<int:request_id>/session/logs', methods=['POST'])
def append_session_log(request_id):
    r = SupportRequest.query.get_or_404(request_id)
    data = request.get_json() or {}
    if not data.get('message'):
        return jsonify({'error': 'message required'}), 400
    meta = None
    try:
        meta = json.dumps(data.get('metadata') or {})
    except Exception:
        meta = None
    entry = SessionLog(request_id=r.id, actor_id=data.get('actor_id'), entry_type=data.get('entry_type','note'), message=data['message'], metadata=meta)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201


# ==================== Health Check & Error Handlers ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-assist'}), 200

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
