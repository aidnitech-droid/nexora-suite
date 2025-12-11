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
        'module': 'nexora-salesiq',
        'status': 'running',
        'endpoints': ['/api/auth/register', '/api/auth/login', '/api/analytics', '/api/health']
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


# ------------------ Chat Widget & Visitor Tracking ------------------

class Visitor(db.Model):
    __tablename__ = 'salesiq_visitors'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    page_url = db.Column(db.Text)
    status = db.Column(db.String(50), default='browsing')  # browsing, waiting, chatting, ended
    created_at = db.Column(db.DateTime, default=db.func.now())
    last_seen = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'page_url': self.page_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class ChatSession(db.Model):
    __tablename__ = 'salesiq_chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('salesiq_visitors.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_key = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    status = db.Column(db.String(50), default='open')  # open, closed, ended
    created_at = db.Column(db.DateTime, default=db.func.now())
    ended_at = db.Column(db.DateTime, nullable=True)

    visitor = db.relationship('Visitor', backref=db.backref('chat_sessions', lazy=True))
    agent = db.relationship('User', backref=db.backref('chats', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'visitor_id': self.visitor_id,
            'agent_id': self.agent_id,
            'session_key': self.session_key,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }


class ChatMessage(db.Model):
    __tablename__ = 'salesiq_messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_session_id = db.Column(db.Integer, db.ForeignKey('salesiq_chat_sessions.id'))
    sender_type = db.Column(db.String(20), default='visitor')  # visitor or agent
    sender_id = db.Column(db.Integer, nullable=True)  # visitor_id or user_id
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    chat_session = db.relationship('ChatSession', backref=db.backref('messages', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'chat_session_id': self.chat_session_id,
            'sender_type': self.sender_type,
            'sender_id': self.sender_id,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


with app.app_context():
    db.create_all()


# Visitor tracking endpoints
@app.route('/api/salesiq/visitors', methods=['POST'])
def create_visitor():
    data = request.get_json() or {}
    v = Visitor(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        ip_address=data.get('ip_address'),
        user_agent=data.get('user_agent'),
        page_url=data.get('page_url'),
        status=data.get('status', 'browsing')
    )
    db.session.add(v)
    db.session.commit()
    return jsonify(v.to_dict()), 201


@app.route('/api/salesiq/visitors', methods=['GET'])
def list_visitors():
    status = request.args.get('status')
    q = Visitor.query
    if status:
        q = q.filter(Visitor.status == status)
    visitors = q.order_by(Visitor.created_at.desc()).all()
    return jsonify([v.to_dict() for v in visitors]), 200


@app.route('/api/salesiq/visitors/<int:visitor_id>', methods=['GET'])
def get_visitor(visitor_id):
    v = Visitor.query.get_or_404(visitor_id)
    return jsonify(v.to_dict()), 200


@app.route('/api/salesiq/visitors/<int:visitor_id>', methods=['PUT'])
def update_visitor(visitor_id):
    v = Visitor.query.get_or_404(visitor_id)
    data = request.get_json() or {}
    v.name = data.get('name', v.name)
    v.email = data.get('email', v.email)
    v.phone = data.get('phone', v.phone)
    v.page_url = data.get('page_url', v.page_url)
    if 'status' in data:
        v.status = data.get('status')
    v.last_seen = datetime.now()
    db.session.commit()
    return jsonify(v.to_dict()), 200


# Chat session endpoints
@app.route('/api/salesiq/chat-sessions', methods=['POST'])
def create_chat_session():
    data = request.get_json() or {}
    visitor_id = data.get('visitor_id')
    if not visitor_id:
        return jsonify({'error': 'visitor_id required'}), 400
    v = Visitor.query.get_or_404(visitor_id)
    chat = ChatSession(visitor_id=visitor_id, agent_id=data.get('agent_id'), status='open')
    v.status = 'chatting'
    db.session.add(chat)
    db.session.commit()
    return jsonify(chat.to_dict()), 201


@app.route('/api/salesiq/chat-sessions/<int:session_id>', methods=['GET'])
def get_chat_session(session_id):
    chat = ChatSession.query.get_or_404(session_id)
    return jsonify(chat.to_dict()), 200


@app.route('/api/salesiq/chat-sessions/<int:session_id>/messages', methods=['GET'])
def get_chat_messages(session_id):
    chat = ChatSession.query.get_or_404(session_id)
    messages = ChatMessage.query.filter(ChatMessage.chat_session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200


@app.route('/api/salesiq/chat-sessions/<int:session_id>/messages', methods=['POST'])
def send_chat_message(session_id):
    chat = ChatSession.query.get_or_404(session_id)
    data = request.get_json() or {}
    if not data.get('message'):
        return jsonify({'error': 'message required'}), 400
    msg = ChatMessage(
        chat_session_id=session_id,
        sender_type=data.get('sender_type', 'visitor'),
        sender_id=data.get('sender_id'),
        message=data['message']
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_dict()), 201


@app.route('/api/salesiq/chat-sessions/<int:session_id>/close', methods=['POST'])
def close_chat_session(session_id):
    chat = ChatSession.query.get_or_404(session_id)
    chat.status = 'closed'
    chat.ended_at = datetime.now()
    if chat.visitor:
        chat.visitor.status = 'ended'
    db.session.commit()
    return jsonify(chat.to_dict()), 200


# Analytics
@app.route('/api/salesiq/analytics', methods=['GET'])
def salesiq_analytics():
    total_visitors = Visitor.query.count()
    active_visitors = Visitor.query.filter(Visitor.status.in_(['browsing', 'chatting'])).count()
    total_chats = ChatSession.query.count()
    open_chats = ChatSession.query.filter(ChatSession.status == 'open').count()
    total_messages = ChatMessage.query.count()
    return jsonify({
        'total_visitors': total_visitors,
        'active_visitors': active_visitors,
        'total_chats': total_chats,
        'open_chats': open_chats,
        'total_messages': total_messages
    }), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-salesiq'}), 200

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
