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

# ==================== Inventory Models ====================

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, default=1000)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    items = db.relationship('Item', backref='warehouse', lazy=True)
    batches = db.relationship('StockBatch', backref='warehouse', lazy=True)


class Item(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    reorder_level = db.Column(db.Integer, default=10)
    reorder_quantity = db.Column(db.Integer, default=50)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    current_stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    batches = db.relationship('StockBatch', backref='item', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('StockAlert', backref='item', lazy=True, cascade='all, delete-orphan')


class StockBatch(db.Model):
    __tablename__ = 'stock_batches'
    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(100), unique=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(12, 2), nullable=False)
    manufacture_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    location_rack = db.Column(db.String(50))
    status = db.Column(db.String(50), default='available')  # available, reserved, expired
    received_date = db.Column(db.DateTime, default=db.func.now())
    created_at = db.Column(db.DateTime, default=db.func.now())


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(100), unique=True, nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(12, 2), nullable=False)
    total_cost = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, received, cancelled
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    order_date = db.Column(db.DateTime, default=db.func.now())
    expected_delivery = db.Column(db.DateTime)
    received_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    item = db.relationship('Item')
    created_at = db.Column(db.DateTime, default=db.func.now())


class SaleOrder(db.Model):
    __tablename__ = 'sale_orders'
    id = db.Column(db.Integer, primary_key=True)
    so_number = db.Column(db.String(100), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    total_price = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, fulfilled, cancelled
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    order_date = db.Column(db.DateTime, default=db.func.now())
    fulfillment_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    item = db.relationship('Item')
    created_at = db.Column(db.DateTime, default=db.func.now())


class StockAlert(db.Model):
    __tablename__ = 'stock_alerts'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    alert_type = db.Column(db.String(50))  # low_stock, expired, overstock
    message = db.Column(db.Text)
    current_stock = db.Column(db.Integer)
    threshold = db.Column(db.Integer)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    resolved_at = db.Column(db.DateTime)

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

# ==================== Warehouse Endpoints ====================

@app.route('/api/warehouses', methods=['GET'])
@jwt_required()
def get_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'location': w.location,
        'capacity': w.capacity,
        'is_active': w.is_active,
        'created_at': w.created_at
    } for w in warehouses]), 200

@app.route('/api/warehouses', methods=['POST'])
@role_required(['admin', 'manager'])
def create_warehouse():
    data = request.get_json()
    
    if not data.get('name') or not data.get('location'):
        return jsonify({'error': 'Name and location are required'}), 400
    
    warehouse = Warehouse(
        name=data['name'],
        location=data['location'],
        capacity=data.get('capacity', 1000),
        manager_id=get_jwt_identity()
    )
    
    db.session.add(warehouse)
    db.session.commit()
    
    return jsonify({
        'id': warehouse.id,
        'name': warehouse.name,
        'location': warehouse.location,
        'capacity': warehouse.capacity
    }), 201

@app.route('/api/warehouses/<int:warehouse_id>', methods=['PUT'])
@role_required(['admin', 'manager'])
def update_warehouse(warehouse_id):
    warehouse = Warehouse.query.get(warehouse_id)
    
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    data = request.get_json()
    warehouse.name = data.get('name', warehouse.name)
    warehouse.location = data.get('location', warehouse.location)
    warehouse.capacity = data.get('capacity', warehouse.capacity)
    warehouse.is_active = data.get('is_active', warehouse.is_active)
    
    db.session.commit()
    
    return jsonify({
        'id': warehouse.id,
        'name': warehouse.name,
        'location': warehouse.location,
        'capacity': warehouse.capacity
    }), 200

# ==================== Item Endpoints ====================

@app.route('/api/items', methods=['GET'])
@jwt_required()
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    warehouse_id = request.args.get('warehouse_id', type=int)
    
    query = Item.query
    if category:
        query = query.filter_by(category=category)
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)
    
    items = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': items.total,
        'pages': items.pages,
        'current_page': page,
        'items': [{
            'id': item.id,
            'sku': item.sku,
            'name': item.name,
            'category': item.category,
            'unit_price': float(item.unit_price),
            'current_stock': item.current_stock,
            'reorder_level': item.reorder_level,
            'warehouse_id': item.warehouse_id,
            'created_at': item.created_at
        } for item in items.items]
    }), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({
        'id': item.id,
        'sku': item.sku,
        'name': item.name,
        'description': item.description,
        'category': item.category,
        'unit_price': float(item.unit_price),
        'current_stock': item.current_stock,
        'reorder_level': item.reorder_level,
        'reorder_quantity': item.reorder_quantity,
        'warehouse_id': item.warehouse_id,
        'batches': len(item.batches),
        'created_at': item.created_at
    }), 200

@app.route('/api/items', methods=['POST'])
@role_required(['admin', 'manager'])
def create_item():
    data = request.get_json()
    
    if not data.get('sku') or not data.get('name') or not data.get('unit_price'):
        return jsonify({'error': 'SKU, name, and price are required'}), 400
    
    if Item.query.filter_by(sku=data['sku']).first():
        return jsonify({'error': 'SKU already exists'}), 409
    
    item = Item(
        sku=data['sku'],
        name=data['name'],
        description=data.get('description'),
        category=data.get('category'),
        unit_price=data['unit_price'],
        reorder_level=data.get('reorder_level', 10),
        reorder_quantity=data.get('reorder_quantity', 50),
        warehouse_id=data.get('warehouse_id')
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'sku': item.sku,
        'name': item.name,
        'unit_price': float(item.unit_price)
    }), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@role_required(['admin', 'manager'])
def update_item(item_id):
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.category = data.get('category', item.category)
    item.unit_price = data.get('unit_price', item.unit_price)
    item.reorder_level = data.get('reorder_level', item.reorder_level)
    item.reorder_quantity = data.get('reorder_quantity', item.reorder_quantity)
    
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'sku': item.sku,
        'name': item.name,
        'unit_price': float(item.unit_price)
    }), 200

# ==================== Stock Batch Endpoints ====================

@app.route('/api/batches', methods=['GET'])
@jwt_required()
def get_batches():
    item_id = request.args.get('item_id', type=int)
    warehouse_id = request.args.get('warehouse_id', type=int)
    status = request.args.get('status')
    
    query = StockBatch.query
    if item_id:
        query = query.filter_by(item_id=item_id)
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)
    if status:
        query = query.filter_by(status=status)
    
    batches = query.all()
    
    return jsonify([{
        'id': b.id,
        'batch_number': b.batch_number,
        'item_id': b.item_id,
        'item_name': b.item.name if b.item else 'Unknown',
        'quantity': b.quantity,
        'unit_cost': float(b.unit_cost),
        'warehouse_id': b.warehouse_id,
        'location_rack': b.location_rack,
        'status': b.status,
        'manufacture_date': b.manufacture_date,
        'expiry_date': b.expiry_date,
        'received_date': b.received_date,
        'created_at': b.created_at
    } for b in batches]), 200

@app.route('/api/batches', methods=['POST'])
@role_required(['admin', 'manager'])
def create_batch():
    data = request.get_json()
    
    required = ['batch_number', 'item_id', 'warehouse_id', 'quantity', 'unit_cost']
    if not all(data.get(field) for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if StockBatch.query.filter_by(batch_number=data['batch_number']).first():
        return jsonify({'error': 'Batch number already exists'}), 409
    
    batch = StockBatch(
        batch_number=data['batch_number'],
        item_id=data['item_id'],
        warehouse_id=data['warehouse_id'],
        quantity=data['quantity'],
        unit_cost=data['unit_cost'],
        manufacture_date=data.get('manufacture_date'),
        expiry_date=data.get('expiry_date'),
        location_rack=data.get('location_rack')
    )
    
    # Update item's current stock
    item = Item.query.get(data['item_id'])
    if item:
        item.current_stock += data['quantity']
    
    db.session.add(batch)
    db.session.commit()
    
    return jsonify({
        'id': batch.id,
        'batch_number': batch.batch_number,
        'quantity': batch.quantity
    }), 201

# ==================== Purchase Order Endpoints ====================

@app.route('/api/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = PurchaseOrder.query
    if status:
        query = query.filter_by(status=status)
    
    orders = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page,
        'orders': [{
            'id': o.id,
            'po_number': o.po_number,
            'supplier_name': o.supplier_name,
            'item_name': o.item.name if o.item else 'Unknown',
            'quantity': o.quantity,
            'unit_cost': float(o.unit_cost),
            'total_cost': float(o.total_cost),
            'status': o.status,
            'order_date': o.order_date,
            'expected_delivery': o.expected_delivery,
            'created_at': o.created_at
        } for o in orders.items]
    }), 200

@app.route('/api/purchase-orders', methods=['POST'])
@role_required(['admin', 'manager'])
def create_purchase_order():
    data = request.get_json()
    
    required = ['po_number', 'supplier_name', 'item_id', 'quantity', 'unit_cost', 'warehouse_id']
    if not all(data.get(field) for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if PurchaseOrder.query.filter_by(po_number=data['po_number']).first():
        return jsonify({'error': 'PO number already exists'}), 409
    
    total_cost = Decimal(data['quantity']) * Decimal(data['unit_cost'])
    
    po = PurchaseOrder(
        po_number=data['po_number'],
        supplier_name=data['supplier_name'],
        item_id=data['item_id'],
        quantity=data['quantity'],
        unit_cost=data['unit_cost'],
        total_cost=total_cost,
        warehouse_id=data['warehouse_id'],
        expected_delivery=data.get('expected_delivery'),
        notes=data.get('notes'),
        created_by=get_jwt_identity()
    )
    
    db.session.add(po)
    db.session.commit()
    
    return jsonify({
        'id': po.id,
        'po_number': po.po_number,
        'total_cost': float(total_cost)
    }), 201

@app.route('/api/purchase-orders/<int:po_id>/receive', methods=['PUT'])
@role_required(['admin', 'manager'])
def receive_purchase_order(po_id):
    po = PurchaseOrder.query.get(po_id)
    
    if not po:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    po.status = 'received'
    po.received_date = datetime.now()
    
    db.session.commit()
    
    return jsonify({'message': 'Purchase order received'}), 200

# ==================== Sale Order Endpoints ====================

@app.route('/api/sale-orders', methods=['GET'])
@jwt_required()
def get_sale_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = SaleOrder.query
    if status:
        query = query.filter_by(status=status)
    
    orders = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page,
        'orders': [{
            'id': o.id,
            'so_number': o.so_number,
            'customer_name': o.customer_name,
            'item_name': o.item.name if o.item else 'Unknown',
            'quantity': o.quantity,
            'unit_price': float(o.unit_price),
            'total_price': float(o.total_price),
            'status': o.status,
            'order_date': o.order_date,
            'fulfillment_date': o.fulfillment_date,
            'created_at': o.created_at
        } for o in orders.items]
    }), 200

@app.route('/api/sale-orders', methods=['POST'])
@role_required(['admin', 'manager'])
def create_sale_order():
    data = request.get_json()
    
    required = ['so_number', 'customer_name', 'item_id', 'quantity', 'unit_price', 'warehouse_id']
    if not all(data.get(field) for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if SaleOrder.query.filter_by(so_number=data['so_number']).first():
        return jsonify({'error': 'Sale order number already exists'}), 409
    
    total_price = Decimal(data['quantity']) * Decimal(data['unit_price'])
    
    so = SaleOrder(
        so_number=data['so_number'],
        customer_name=data['customer_name'],
        item_id=data['item_id'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        total_price=total_price,
        warehouse_id=data['warehouse_id'],
        notes=data.get('notes'),
        created_by=get_jwt_identity()
    )
    
    db.session.add(so)
    db.session.commit()
    
    return jsonify({
        'id': so.id,
        'so_number': so.so_number,
        'total_price': float(total_price)
    }), 201

@app.route('/api/sale-orders/<int:so_id>/fulfill', methods=['PUT'])
@role_required(['admin', 'manager'])
def fulfill_sale_order(so_id):
    so = SaleOrder.query.get(so_id)
    
    if not so:
        return jsonify({'error': 'Sale order not found'}), 404
    
    # Check if stock is available
    item = so.item
    if item.current_stock < so.quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Update stock
    item.current_stock -= so.quantity
    so.status = 'fulfilled'
    so.fulfillment_date = datetime.now()
    
    db.session.commit()
    
    return jsonify({'message': 'Sale order fulfilled'}), 200

# ==================== Stock Alert Endpoints ====================

@app.route('/api/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    resolved = request.args.get('resolved', 'false').lower() == 'true'
    alert_type = request.args.get('alert_type')
    
    query = StockAlert.query.filter_by(is_resolved=resolved)
    if alert_type:
        query = query.filter_by(alert_type=alert_type)
    
    alerts = query.order_by(StockAlert.created_at.desc()).all()
    
    return jsonify([{
        'id': a.id,
        'item_id': a.item_id,
        'item_name': a.item.name if a.item else 'Unknown',
        'alert_type': a.alert_type,
        'message': a.message,
        'current_stock': a.current_stock,
        'threshold': a.threshold,
        'is_resolved': a.is_resolved,
        'created_at': a.created_at
    } for a in alerts]), 200

@app.route('/api/alerts', methods=['POST'])
@role_required(['admin', 'manager'])
def create_alert():
    data = request.get_json()
    
    if not data.get('item_id') or not data.get('alert_type'):
        return jsonify({'error': 'Item ID and alert type are required'}), 400
    
    alert = StockAlert(
        item_id=data['item_id'],
        alert_type=data['alert_type'],
        message=data.get('message'),
        current_stock=data.get('current_stock'),
        threshold=data.get('threshold')
    )
    
    db.session.add(alert)
    db.session.commit()
    
    return jsonify({
        'id': alert.id,
        'alert_type': alert.alert_type
    }), 201

@app.route('/api/alerts/<int:alert_id>/resolve', methods=['PUT'])
@role_required(['admin', 'manager'])
def resolve_alert(alert_id):
    alert = StockAlert.query.get(alert_id)
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    alert.is_resolved = True
    alert.resolved_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({'message': 'Alert resolved'}), 200

# ==================== Check and Create Alerts ====================

def check_stock_levels():
    """Automatically check stock levels and create alerts"""
    items = Item.query.all()
    
    for item in items:
        # Check for low stock
        if item.current_stock <= item.reorder_level:
            existing_alert = StockAlert.query.filter_by(
                item_id=item.id,
                alert_type='low_stock',
                is_resolved=False
            ).first()
            
            if not existing_alert:
                alert = StockAlert(
                    item_id=item.id,
                    alert_type='low_stock',
                    message=f'Stock level for {item.name} is below reorder level',
                    current_stock=item.current_stock,
                    threshold=item.reorder_level
                )
                db.session.add(alert)
        
        # Check for expired batches
        for batch in item.batches:
            if batch.expiry_date and batch.expiry_date < datetime.now() and batch.status != 'expired':
                existing_alert = StockAlert.query.filter_by(
                    item_id=item.id,
                    alert_type='expired',
                    is_resolved=False
                ).first()
                
                if not existing_alert:
                    alert = StockAlert(
                        item_id=item.id,
                        alert_type='expired',
                        message=f'Batch {batch.batch_number} for {item.name} has expired'
                    )
                    db.session.add(alert)
                
                batch.status = 'expired'
    
    db.session.commit()

# ==================== Analytics Endpoints ====================

@app.route('/api/analytics/summary', methods=['GET'])
@jwt_required()
def get_analytics_summary():
    """Get inventory analytics summary"""
    
    total_items = Item.query.count()
    total_warehouses = Warehouse.query.count()
    total_stock_value = db.session.query(
        db.func.sum(Item.current_stock * Item.unit_price)
    ).scalar() or 0
    
    low_stock_items = Item.query.filter(Item.current_stock <= Item.reorder_level).count()
    pending_pos = PurchaseOrder.query.filter_by(status='pending').count()
    pending_sos = SaleOrder.query.filter_by(status='pending').count()
    active_alerts = StockAlert.query.filter_by(is_resolved=False).count()
    
    return jsonify({
        'total_items': total_items,
        'total_warehouses': total_warehouses,
        'total_stock_value': float(total_stock_value),
        'low_stock_items': low_stock_items,
        'pending_purchase_orders': pending_pos,
        'pending_sale_orders': pending_sos,
        'active_alerts': active_alerts
    }), 200

@app.route('/api/analytics/stock-value', methods=['GET'])
@jwt_required()
def get_stock_value_by_category():
    """Get stock value breakdown by category"""
    
    categories = db.session.query(
        Item.category,
        db.func.sum(Item.current_stock * Item.unit_price).label('total_value'),
        db.func.sum(Item.current_stock).label('total_quantity')
    ).group_by(Item.category).all()
    
    return jsonify([{
        'category': cat[0] or 'Uncategorized',
        'total_value': float(cat[1] or 0),
        'total_quantity': cat[2] or 0
    } for cat in categories]), 200

@app.route('/api/analytics/warehouse-capacity', methods=['GET'])
@jwt_required()
def get_warehouse_capacity():
    """Get warehouse utilization data"""
    
    warehouses = Warehouse.query.all()
    data = []
    
    for warehouse in warehouses:
        total_items = db.session.query(
            db.func.sum(Item.current_stock)
        ).filter(Item.warehouse_id == warehouse.id).scalar() or 0
        
        utilization = (total_items / warehouse.capacity * 100) if warehouse.capacity > 0 else 0
        
        data.append({
            'warehouse_id': warehouse.id,
            'warehouse_name': warehouse.name,
            'capacity': warehouse.capacity,
            'current_usage': total_items,
            'utilization_percent': round(utilization, 2)
        })
    
    return jsonify(data), 200

@app.route('/api/analytics/movement', methods=['GET'])
@jwt_required()
def get_inventory_movement():
    """Get purchase and sale trends"""
    
    pos = db.session.query(
        db.func.count(PurchaseOrder.id).label('count'),
        db.func.sum(PurchaseOrder.total_cost).label('total_cost')
    ).filter(PurchaseOrder.status == 'received').first()
    
    sos = db.session.query(
        db.func.count(SaleOrder.id).label('count'),
        db.func.sum(SaleOrder.total_price).label('total_revenue')
    ).filter(SaleOrder.status == 'fulfilled').first()
    
    return jsonify({
        'purchase_orders': {
            'count': pos[0] or 0,
            'total_cost': float(pos[1] or 0)
        },
        'sale_orders': {
            'count': sos[0] or 0,
            'total_revenue': float(sos[1] or 0)
        }
    }), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-inventory'}), 200

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
        check_stock_levels()
    app.run(debug=True, host='0.0.0.0', port=5000)
