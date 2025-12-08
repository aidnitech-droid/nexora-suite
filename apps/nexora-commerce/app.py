from flask import Flask, jsonify, request, abort
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


# ------------------- Commerce Models -------------------
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return { 'id': self.id, 'name': self.name, 'description': self.description }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(12,2), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'quantity': self.quantity,
            'category': self.category.to_dict() if self.category else None
        }

class StorefrontTemplate(db.Model):
    __tablename__ = 'storefront_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    html = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return { 'id': self.id, 'name': self.name, 'slug': self.slug, 'html': self.html, 'created_at': self.created_at }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(80), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Numeric(12,2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.now())

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(12,2), nullable=False)

    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product')

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


# ------------------- Commerce Endpoints -------------------
@app.route('/api/categories', methods=['GET'])
def list_categories():
    cats = Category.query.order_by(Category.name).all()
    return jsonify([c.to_dict() for c in cats]), 200


@app.route('/api/categories', methods=['POST'])
@role_required(['admin','manager'])
def create_category():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name required'}), 400
    cat = Category(name=name, description=data.get('description'))
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201


@app.route('/api/products', methods=['GET'])
def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    q = Product.query
    cat = request.args.get('category')
    if cat:
        # allow category id or name
        if cat.isdigit():
            q = q.filter(Product.category_id==int(cat))
        else:
            q = q.join(Category).filter(Category.name.ilike(f"%{cat}%"))
    items = q.order_by(Product.name).paginate(page=page, per_page=per_page)
    return jsonify({
        'items': [p.to_dict() for p in items.items],
        'current_page': items.page,
        'pages': items.pages,
        'total': items.total
    }), 200


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Product.query.get_or_404(product_id)
    return jsonify(p.to_dict()), 200


@app.route('/api/products', methods=['POST'])
@role_required(['admin','manager'])
def create_product():
    data = request.get_json() or {}
    required = ['sku','name','price']
    for r in required:
        if r not in data:
            return jsonify({'error': f'{r} required'}), 400
    cat = None
    if data.get('category_id'):
        cat = Category.query.get(data.get('category_id'))
    p = Product(
        sku=data['sku'],
        name=data['name'],
        description=data.get('description'),
        price=Decimal(str(data['price'])),
        quantity=int(data.get('quantity',0)),
        category=cat
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json() or {}
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    items = data.get('items', [])
    if not customer_name or not customer_email or not items:
        return jsonify({'error': 'customer_name, customer_email and items are required'}), 400

    total = Decimal('0.00')
    for it in items:
        pid = it.get('product_id')
        qty = int(it.get('quantity', 0))
        product = Product.query.get(pid)
        if not product:
            return jsonify({'error': f'product {pid} not found'}), 400
        if product.quantity < qty:
            return jsonify({'error': f'not enough stock for product {product.name}'}), 400
        total += Decimal(str(product.price)) * qty

    order = Order(
        order_number=f"ORD-{int(datetime.utcnow().timestamp())}",
        customer_name=customer_name,
        customer_email=customer_email,
        total_amount=total,
        status='pending'
    )
    db.session.add(order)
    db.session.flush()

    for it in items:
        pid = it.get('product_id')
        qty = int(it.get('quantity', 0))
        product = Product.query.get(pid)
        oi = OrderItem(order_id=order.id, product_id=product.id, quantity=qty, unit_price=product.price)
        product.quantity = product.quantity - qty
        db.session.add(oi)

    db.session.commit()
    return jsonify({'order_id': order.id, 'order_number': order.order_number, 'total': str(order.total_amount)}), 201


@app.route('/api/storefronts', methods=['GET'])
def list_storefronts():
    t = StorefrontTemplate.query.order_by(StorefrontTemplate.created_at.desc()).all()
    return jsonify([s.to_dict() for s in t]), 200


@app.route('/api/storefronts', methods=['POST'])
@role_required(['admin','manager'])
def create_storefront():
    data = request.get_json() or {}
    name = data.get('name')
    slug = data.get('slug')
    html = data.get('html','')
    if not name or not slug:
        return jsonify({'error': 'name and slug required'}), 400
    s = StorefrontTemplate(name=name, slug=slug, html=html)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201


@app.route('/store/<slug>', methods=['GET'])
def render_storefront(slug):
    s = StorefrontTemplate.query.filter_by(slug=slug).first()
    if not s:
        return jsonify({'error': 'storefront not found'}), 404
    # For simple template rendering we return HTML content stored in template
    return s.html or ('<h1>' + s.name + '</h1>'), 200

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
    return jsonify({'status': 'healthy', 'service': 'nexora-commerce'}), 200

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
