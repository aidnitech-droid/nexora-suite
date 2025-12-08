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

# ------------------ Support Desk Models & Endpoints ------------------

class TicketCategory(db.Model):
    __tablename__ = 'desk_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'created_at': self.created_at.isoformat()}


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    customer_name = db.Column(db.String(255))
    customer_email = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('desk_categories.id'), nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low/medium/high
    status = db.Column(db.String(50), default='open')  # open/assigned/in_progress/resolved/closed
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    category = db.relationship('TicketCategory')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'category': self.category.to_dict() if self.category else None,
            'category_id': self.category_id,
            'priority': self.priority,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TicketComment(db.Model):
    __tablename__ = 'ticket_comments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_tickets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    ticket = db.relationship('SupportTicket', backref=db.backref('comments', lazy=True))

    def to_dict(self):
        return {'id': self.id, 'ticket_id': self.ticket_id, 'user_id': self.user_id, 'message': self.message, 'created_at': self.created_at.isoformat()}


with app.app_context():
    db.create_all()


# Category endpoints
@app.route('/api/desk/categories', methods=['GET'])
def list_categories():
    cats = TicketCategory.query.order_by(TicketCategory.name).all()
    return jsonify([c.to_dict() for c in cats]), 200


@app.route('/api/desk/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    c = TicketCategory(name=data['name'], description=data.get('description'))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route('/api/desk/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    c = TicketCategory.query.get_or_404(cat_id)
    data = request.get_json() or {}
    c.name = data.get('name', c.name)
    c.description = data.get('description', c.description)
    db.session.commit()
    return jsonify(c.to_dict()), 200


@app.route('/api/desk/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    c = TicketCategory.query.get_or_404(cat_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'category deleted'}), 200


# Ticket endpoints
@app.route('/api/desk/tickets', methods=['GET'])
def list_tickets():
    status = request.args.get('status')
    category = request.args.get('category_id', type=int)
    assigned = request.args.get('assigned_to', type=int)
    q = SupportTicket.query
    if status:
        q = q.filter(SupportTicket.status == status)
    if category:
        q = q.filter(SupportTicket.category_id == category)
    if assigned:
        q = q.filter(SupportTicket.assigned_to == assigned)
    tickets = q.order_by(SupportTicket.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tickets]), 200


@app.route('/api/desk/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    return jsonify(t.to_dict()), 200


@app.route('/api/desk/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title required'}), 400
    t = SupportTicket(
        title=data['title'],
        description=data.get('description'),
        customer_name=data.get('customer_name'),
        customer_email=data.get('customer_email'),
        category_id=data.get('category_id'),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        assigned_to=data.get('assigned_to'),
        created_by=data.get('created_by')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.route('/api/desk/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    t.title = data.get('title', t.title)
    t.description = data.get('description', t.description)
    t.customer_name = data.get('customer_name', t.customer_name)
    t.customer_email = data.get('customer_email', t.customer_email)
    t.category_id = data.get('category_id', t.category_id)
    t.priority = data.get('priority', t.priority)
    if data.get('status'):
        t.status = data.get('status')
    db.session.commit()
    return jsonify(t.to_dict()), 200


@app.route('/api/desk/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    # delete comments first
    for c in t.comments:
        db.session.delete(c)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'ticket deleted'}), 200


# Assign technician
@app.route('/api/desk/tickets/<int:ticket_id>/assign', methods=['POST'])
def assign_ticket(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    user_id = data.get('assigned_to')
    if not user_id:
        return jsonify({'error': 'assigned_to required'}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    t.assigned_to = user_id
    t.status = data.get('status', 'assigned')
    db.session.commit()
    return jsonify(t.to_dict()), 200


# Status update
@app.route('/api/desk/tickets/<int:ticket_id>/status', methods=['POST'])
def change_ticket_status(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    status = data.get('status')
    if not status:
        return jsonify({'error': 'status required'}), 400
    t.status = status
    db.session.commit()
    return jsonify(t.to_dict()), 200


# Comments
@app.route('/api/desk/tickets/<int:ticket_id>/comments', methods=['GET'])
def list_comments(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    return jsonify([c.to_dict() for c in t.comments]), 200


@app.route('/api/desk/tickets/<int:ticket_id>/comments', methods=['POST'])
def add_comment(ticket_id):
    t = SupportTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    if not data.get('message'):
        return jsonify({'error': 'message required'}), 400
    comment = TicketComment(ticket_id=t.id, user_id=data.get('user_id'), message=data['message'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201


# Analytics
@app.route('/api/desk/analytics', methods=['GET'])
def desk_analytics():
    total = SupportTicket.query.count()
    by_status = db.session.query(SupportTicket.status, db.func.count(SupportTicket.id)).group_by(SupportTicket.status).all()
    by_category = db.session.query(TicketCategory.name, db.func.count(SupportTicket.id)).join(SupportTicket, SupportTicket.category_id == TicketCategory.id, isouter=True).group_by(TicketCategory.name).all()
    return jsonify({'total': total, 'by_status': [{'status': s, 'count': c} for s,c in by_status], 'by_category': [{'category': n, 'count': c} for n,c in by_category]}), 200


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-desk'}), 200

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
