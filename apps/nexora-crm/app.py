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


# ---------------- CRM Models ----------------
class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    source = db.Column(db.String(100))
    status = db.Column(db.String(50), default='new')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'source': self.source,
            'status': self.status,
            'created_at': self.created_at
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())

    lead = db.relationship('Lead', backref=db.backref('contacts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'created_at': self.created_at
        }

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    amount = db.Column(db.Numeric(12,2), default=0)
    stage = db.Column(db.String(100), default='prospect')
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=db.func.now())

    contact = db.relationship('Contact', backref=db.backref('deals', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'contact_id': self.contact_id,
            'amount': str(self.amount),
            'stage': self.stage,
            'status': self.status,
            'created_at': self.created_at
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    related_type = db.Column(db.String(50))  # 'lead','contact','deal'
    related_id = db.Column(db.Integer)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='todo')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'related_type': self.related_type,
            'related_id': self.related_id,
            'due_date': self.due_date,
            'status': self.status,
            'created_at': self.created_at
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

# ---------------- CRM Endpoints ----------------

# Leads
@app.route('/api/leads', methods=['GET'])
def list_leads():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    q = Lead.query.order_by(Lead.created_at.desc())
    leads = q.paginate(page=page, per_page=per_page)
    return jsonify({
        'leads': [l.to_dict() for l in leads.items],
        'current_page': leads.page,
        'pages': leads.pages,
        'total': leads.total
    }), 200


@app.route('/api/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    l = Lead.query.get_or_404(lead_id)
    return jsonify(l.to_dict()), 200


@app.route('/api/leads', methods=['POST'])
@role_required(['admin','manager'])
def create_lead():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    l = Lead(name=data['name'], email=data.get('email'), phone=data.get('phone'), source=data.get('source'))
    db.session.add(l)
    db.session.commit()
    return jsonify(l.to_dict()), 201


@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
@role_required(['admin','manager'])
def update_lead(lead_id):
    l = Lead.query.get_or_404(lead_id)
    data = request.get_json() or {}
    l.name = data.get('name', l.name)
    l.email = data.get('email', l.email)
    l.phone = data.get('phone', l.phone)
    l.source = data.get('source', l.source)
    l.status = data.get('status', l.status)
    db.session.commit()
    return jsonify(l.to_dict()), 200


@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_lead(lead_id):
    l = Lead.query.get_or_404(lead_id)
    db.session.delete(l)
    db.session.commit()
    return jsonify({'message': 'Lead deleted'}), 200


# Contacts
@app.route('/api/contacts', methods=['GET'])
def list_contacts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    q = Contact.query.order_by(Contact.created_at.desc())
    contacts = q.paginate(page=page, per_page=per_page)
    return jsonify({
        'contacts': [c.to_dict() for c in contacts.items],
        'current_page': contacts.page,
        'pages': contacts.pages,
        'total': contacts.total
    }), 200


@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    c = Contact.query.get_or_404(contact_id)
    return jsonify(c.to_dict()), 200


@app.route('/api/contacts', methods=['POST'])
@role_required(['admin','manager'])
def create_contact():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    c = Contact(lead_id=data.get('lead_id'), name=data['name'], email=data.get('email'), phone=data.get('phone'), company=data.get('company'))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
@role_required(['admin','manager'])
def update_contact(contact_id):
    c = Contact.query.get_or_404(contact_id)
    data = request.get_json() or {}
    c.name = data.get('name', c.name)
    c.email = data.get('email', c.email)
    c.phone = data.get('phone', c.phone)
    c.company = data.get('company', c.company)
    db.session.commit()
    return jsonify(c.to_dict()), 200


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_contact(contact_id):
    c = Contact.query.get_or_404(contact_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'}), 200


# Deals
@app.route('/api/deals', methods=['GET'])
def list_deals():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    stage = request.args.get('stage')
    q = Deal.query
    if stage:
        q = q.filter(Deal.stage == stage)
    deals = q.order_by(Deal.created_at.desc()).paginate(page=page, per_page=per_page)
    return jsonify({
        'deals': [d.to_dict() for d in deals.items],
        'current_page': deals.page,
        'pages': deals.pages,
        'total': deals.total
    }), 200


@app.route('/api/deals/<int:deal_id>', methods=['GET'])
def get_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    return jsonify(d.to_dict()), 200


@app.route('/api/deals', methods=['POST'])
@role_required(['admin','manager'])
def create_deal():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title required'}), 400
    amount = Decimal(str(data.get('amount', '0')))
    d = Deal(title=data['title'], contact_id=data.get('contact_id'), amount=amount, stage=data.get('stage','prospect'))
    db.session.add(d)
    db.session.commit()
    return jsonify(d.to_dict()), 201


@app.route('/api/deals/<int:deal_id>', methods=['PUT'])
@role_required(['admin','manager'])
def update_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    data = request.get_json() or {}
    d.title = data.get('title', d.title)
    d.amount = Decimal(str(data.get('amount', d.amount)))
    d.stage = data.get('stage', d.stage)
    d.status = data.get('status', d.status)
    db.session.commit()
    return jsonify(d.to_dict()), 200


@app.route('/api/deals/<int:deal_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_deal(deal_id):
    d = Deal.query.get_or_404(deal_id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Deal deleted'}), 200


# Tasks
@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    q = Task.query.order_by(Task.due_date.asc().nulls_last())
    tasks = q.paginate(page=page, per_page=per_page)
    return jsonify({
        'tasks': [t.to_dict() for t in tasks.items],
        'current_page': tasks.page,
        'pages': tasks.pages,
        'total': tasks.total
    }), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    t = Task.query.get_or_404(task_id)
    return jsonify(t.to_dict()), 200


@app.route('/api/tasks', methods=['POST'])
@role_required(['admin','manager'])
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
    t = Task(title=data['title'], description=data.get('description'), assigned_to=data.get('assigned_to'), related_type=data.get('related_type'), related_id=data.get('related_id'), due_date=due)
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@role_required(['admin','manager'])
def update_task(task_id):
    t = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    t.title = data.get('title', t.title)
    t.description = data.get('description', t.description)
    t.status = data.get('status', t.status)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200


# Analytics / Dashboard
@app.route('/api/crm/analytics', methods=['GET'])
def crm_analytics():
    total_leads = Lead.query.count()
    total_contacts = Contact.query.count()
    total_deals = Deal.query.count()
    open_deals = Deal.query.filter(Deal.status=='open').count()
    closed_deals = Deal.query.filter(Deal.status=='closed').count()
    # pipeline breakdown
    stages = db.session.query(Deal.stage, db.func.count(Deal.id)).group_by(Deal.stage).all()
    pipeline = [{ 'stage': s, 'count': c } for s,c in stages]
    return jsonify({
        'total_leads': total_leads,
        'total_contacts': total_contacts,
        'total_deals': total_deals,
        'open_deals': open_deals,
        'closed_deals': closed_deals,
        'pipeline': pipeline
    }), 200


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-crm'}), 200

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
