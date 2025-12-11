from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta, datetime
from decimal import Decimal
import io

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

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
        'module': 'nexora-invoice',
        'status': 'running',
        'endpoints': ['/api/auth/register', '/api/auth/login', '/api/invoices', '/api/health']
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

# ------------------ Invoice Module Models & Endpoints ------------------

class Customer(db.Model):
    __tablename__ = 'invoice_customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Item(db.Model):
    __tablename__ = 'invoice_items'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(80), unique=True, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    unit_price = db.Column(db.Numeric(12,2), default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'unit_price': str(self.unit_price),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(80), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('invoice_customers.id'))
    date = db.Column(db.DateTime, default=db.func.now())
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('invoices', lazy=True))

    def to_dict(self):
        items = [ii.to_dict() for ii in self.items]
        subtotal = sum(Decimal(ii['total']) for ii in items) if items else Decimal('0')
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'items': items,
            'subtotal': str(subtotal),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class InvoiceItem(db.Model):
    __tablename__ = 'invoice_invoice_items'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('invoice_items.id'))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(12,2), default=0)

    invoice = db.relationship('Invoice', backref=db.backref('items', lazy=True))
    item = db.relationship('Item')

    def to_dict(self):
        total = Decimal(self.quantity) * Decimal(str(self.unit_price))
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'item_id': self.item_id,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': str(self.unit_price),
            'total': str(total)
        }


with app.app_context():
    db.create_all()


# Customer endpoints
@app.route('/api/invoice/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers]), 200


@app.route('/api/invoice/customers', methods=['POST'])
def create_customer():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    c = Customer(name=data['name'], email=data.get('email'), phone=data.get('phone'), address=data.get('address'))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route('/api/invoice/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    return jsonify(c.to_dict()), 200


@app.route('/api/invoice/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    c.name = data.get('name', c.name)
    c.email = data.get('email', c.email)
    c.phone = data.get('phone', c.phone)
    c.address = data.get('address', c.address)
    db.session.commit()
    return jsonify(c.to_dict()), 200


@app.route('/api/invoice/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'customer deleted'}), 200


# Item endpoints
@app.route('/api/invoice/items', methods=['GET'])
def list_invoice_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([i.to_dict() for i in items]), 200


@app.route('/api/invoice/items', methods=['POST'])
def create_invoice_item():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    try:
        unit_price = Decimal(str(data.get('unit_price', '0')))
    except Exception:
        unit_price = Decimal('0')
    it = Item(sku=data.get('sku'), name=data['name'], description=data.get('description'), unit_price=unit_price)
    db.session.add(it)
    db.session.commit()
    return jsonify(it.to_dict()), 201


@app.route('/api/invoice/items/<int:item_id>', methods=['GET'])
def get_invoice_item(item_id):
    it = Item.query.get_or_404(item_id)
    return jsonify(it.to_dict()), 200


@app.route('/api/invoice/items/<int:item_id>', methods=['PUT'])
def update_invoice_item(item_id):
    it = Item.query.get_or_404(item_id)
    data = request.get_json() or {}
    it.name = data.get('name', it.name)
    it.description = data.get('description', it.description)
    try:
        it.unit_price = Decimal(str(data.get('unit_price', it.unit_price)))
    except Exception:
        pass
    it.sku = data.get('sku', it.sku)
    db.session.commit()
    return jsonify(it.to_dict()), 200


@app.route('/api/invoice/items/<int:item_id>', methods=['DELETE'])
def delete_invoice_item(item_id):
    it = Item.query.get_or_404(item_id)
    db.session.delete(it)
    db.session.commit()
    return jsonify({'message': 'item deleted'}), 200


# Invoice endpoints
@app.route('/api/invoice/invoices', methods=['GET'])
def list_invoices():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices]), 200


@app.route('/api/invoice/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    return jsonify(inv.to_dict()), 200


@app.route('/api/invoice/invoices', methods=['POST'])
def create_invoice():
    data = request.get_json() or {}
    if not data.get('invoice_number') or not data.get('customer_id'):
        return jsonify({'error': 'invoice_number and customer_id required'}), 400
    inv = Invoice(invoice_number=data['invoice_number'], customer_id=data['customer_id'], notes=data.get('notes'))
    db.session.add(inv)
    db.session.flush()  # get id before adding items

    items = data.get('items', [])
    for it in items:
        try:
            unit_price = Decimal(str(it.get('unit_price', '0')))
        except Exception:
            unit_price = Decimal('0')
        qty = int(it.get('quantity', 1))
        desc = it.get('description') or it.get('name') or ''
        ii = InvoiceItem(invoice_id=inv.id, item_id=it.get('item_id'), description=desc, quantity=qty, unit_price=unit_price)
        db.session.add(ii)

    db.session.commit()
    return jsonify(inv.to_dict()), 201


@app.route('/api/invoice/invoices/<int:invoice_id>/pdf', methods=['GET'])
def invoice_pdf(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    # Build PDF in-memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    x = margin
    y = height - margin

    # Header
    p.setFont('Helvetica-Bold', 16)
    p.drawString(x, y, f"Invoice: {inv.invoice_number}")
    p.setFont('Helvetica', 10)
    p.drawString(x, y - 18, f"Date: {inv.date.strftime('%Y-%m-%d') if inv.date else ''}")
    if inv.customer:
        p.drawString(x, y - 36, f"Bill To: {inv.customer.name}")
        if inv.customer.address:
            p.drawString(x, y - 50, inv.customer.address[:100])

    # Items table header
    table_y = y - 90
    p.setFont('Helvetica-Bold', 10)
    p.drawString(x, table_y, 'Qty')
    p.drawString(x + 30 * mm, table_y, 'Description')
    p.drawString(x + 110 * mm, table_y, 'Unit')
    p.drawString(x + 140 * mm, table_y, 'Total')
    p.setFont('Helvetica', 10)

    cur_y = table_y - 18
    subtotal = Decimal('0')
    for ii in inv.items:
        line_total = Decimal(ii.quantity) * Decimal(str(ii.unit_price))
        subtotal += line_total
        p.drawString(x, cur_y, str(ii.quantity))
        p.drawString(x + 30 * mm, cur_y, (ii.description or '')[:60])
        p.drawString(x + 110 * mm, cur_y, str(ii.unit_price))
        p.drawString(x + 140 * mm, cur_y, str(line_total))
        cur_y -= 14
        if cur_y < margin + 40:
            p.showPage()
            cur_y = height - margin

    # Totals
    p.setFont('Helvetica-Bold', 11)
    p.drawString(x + 110 * mm, cur_y - 10, 'Subtotal:')
    p.drawString(x + 140 * mm, cur_y - 10, str(subtotal))

    if inv.notes:
        p.setFont('Helvetica', 9)
        p.drawString(x, cur_y - 40, 'Notes:')
        p.drawString(x, cur_y - 54, (inv.notes or '')[:200])

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f"invoice_{inv.invoice_number}.pdf")


@app.route('/api/invoice/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    # delete items first
    for ii in inv.items:
        db.session.delete(ii)
    db.session.delete(inv)
    db.session.commit()
    return jsonify({'message': 'invoice deleted'}), 200


# ==================== Health & Error Handlers ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-invoice'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5021)
