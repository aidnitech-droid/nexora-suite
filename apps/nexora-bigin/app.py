from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta, datetime
from decimal import Decimal

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


# ==================== Bigin Models ====================

class Deal(db.Model):
    __tablename__ = 'bigin_deals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(12,2), default=0)
    stage = db.Column(db.String(100), default='prospect')
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': str(self.amount),
            'stage': self.stage,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Task(db.Model):
    __tablename__ = 'bigin_tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    related_deal_id = db.Column(db.Integer, db.ForeignKey('bigin_deals.id'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='todo')
    created_at = db.Column(db.DateTime, default=db.func.now())

    deal = db.relationship('Deal', backref=db.backref('tasks', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'related_deal_id': self.related_deal_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

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
        'module': 'nexora-bigin',
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

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-bigin'}), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== Bigin Endpoints ====================


@app.route('/api/bigin/deals', methods=['GET'])
def list_deals():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    stage = request.args.get('stage')
    q = Deal.query
    if stage:
        q = q.filter(Deal.stage == stage)
    items = q.order_by(Deal.created_at.desc()).paginate(page=page, per_page=per_page)
    return jsonify({
        'deals': [d.to_dict() for d in items.items],
        'current_page': items.page,
        'pages': items.pages,
        'total': items.total
    }), 200


@app.route('/api/bigin/deals/<int:deal_id>', methods=['GET'])
def get_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    return jsonify(d.to_dict()), 200


@app.route('/api/bigin/deals', methods=['POST'])
def create_deal():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title required'}), 400
    amount = data.get('amount', 0)
    try:
        amount = Decimal(str(amount))
    except Exception:
        amount = Decimal('0')
    d = Deal(title=data['title'], amount=amount, stage=data.get('stage','prospect'))
    db.session.add(d)
    db.session.commit()
    return jsonify(d.to_dict()), 201


@app.route('/api/bigin/deals/<int:deal_id>', methods=['PUT'])
def update_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    data = request.get_json() or {}
    d.title = data.get('title', d.title)
    if 'amount' in data:
        try:
            d.amount = Decimal(str(data.get('amount', d.amount)))
        except Exception:
            pass
    d.stage = data.get('stage', d.stage)
    d.status = data.get('status', d.status)
    db.session.commit()
    return jsonify(d.to_dict()), 200


@app.route('/api/bigin/deals/<int:deal_id>', methods=['DELETE'])
def delete_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Deal deleted'}), 200


# Tasks endpoints
@app.route('/api/bigin/tasks', methods=['GET'])
def list_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    related = request.args.get('related_deal_id', type=int)
    q = Task.query
    if related:
        q = q.filter(Task.related_deal_id == related)
    items = q.order_by(Task.due_date.asc().nulls_last()).paginate(page=page, per_page=per_page)
    return jsonify({
        'tasks': [t.to_dict() for t in items.items],
        'current_page': items.page,
        'pages': items.pages,
        'total': items.total
    }), 200


@app.route('/api/bigin/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    t = Task.query.get_or_404(task_id)
    return jsonify(t.to_dict()), 200


@app.route('/api/bigin/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title required'}), 400
    due = None
    if data.get('due_date'):
        try:
            due = datetime.fromisoformat(data.get('due_date'))
        except Exception:
            due = None
    t = Task(title=data['title'], description=data.get('description'), related_deal_id=data.get('related_deal_id'), due_date=due)
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.route('/api/bigin/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    t = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    t.title = data.get('title', t.title)
    t.description = data.get('description', t.description)
    t.status = data.get('status', t.status)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@app.route('/api/bigin/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200


# Pipeline summary
@app.route('/api/bigin/pipeline', methods=['GET'])
def pipeline_summary():
    total_deals = Deal.query.count()
    by_stage = db.session.query(Deal.stage, db.func.count(Deal.id)).group_by(Deal.stage).all()
    stages = [{'stage': s, 'count': c} for s,c in by_stage]
    open_deals = Deal.query.filter(Deal.status=='open').count()
    closed_deals = Deal.query.filter(Deal.status=='closed').count()
    return jsonify({
        'total_deals': total_deals,
        'open_deals': open_deals,
        'closed_deals': closed_deals,
        'stages': stages
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
