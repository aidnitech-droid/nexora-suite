from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import send_from_directory
import uuid

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

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


# -------------------- Expense Models --------------------
class Category(db.Model):
    __tablename__ = 'expense_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())


class ExpenseReport(db.Model):
    __tablename__ = 'expense_reports'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    date = db.Column(db.DateTime, default=db.func.now())
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='draft')
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    attachments = db.relationship('Attachment', backref='expense', lazy=True)


class Attachment(db.Model):
    __tablename__ = 'expense_attachments'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(1024), nullable=False)
    mimetype = db.Column(db.String(255))
    expense_id = db.Column(db.Integer, db.ForeignKey('expense_reports.id'))
    uploaded_at = db.Column(db.DateTime, default=db.func.now())

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
        'module': 'nexora-expense',
        'status': 'running',
        'endpoints': ['/api/auth/register', '/api/auth/login', '/api/expenses', '/api/health']
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

# ==================== CRUD Endpoints - Generic Items ====================

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

# ==================== CRUD Endpoints - Categories ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'created_at': cat.created_at
    } for cat in categories]), 200

@app.route('/api/categories', methods=['POST'])
@role_required(['admin', 'manager'])
def create_category():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400
    
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 409
    
    category = Category(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    }), 201

@app.route('/api/categories/<int:cat_id>', methods=['PUT'])
@role_required(['admin', 'manager'])
def update_category(cat_id):
    category = Category.query.get(cat_id)
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    data = request.get_json()
    
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    }), 200

@app.route('/api/categories/<int:cat_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_category(cat_id):
    category = Category.query.get(cat_id)
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'}), 200

# ==================== CRUD Endpoints - Expense Reports ====================

@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', None)
    category_id = request.args.get('category_id', None, type=int)
    
    query = ExpenseReport.query
    
    if status:
        query = query.filter_by(status=status)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    expenses = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': expenses.total,
        'pages': expenses.pages,
        'current_page': page,
        'expenses': [{
            'id': exp.id,
            'title': exp.title,
            'amount': float(exp.amount),
            'date': exp.date,
            'description': exp.description,
            'status': exp.status,
            'category_id': exp.category_id,
            'attachments': [{
                'id': att.id,
                'filename': att.filename,
                'url': f'/api/attachments/{att.id}'
            } for att in exp.attachments],
            'created_at': exp.created_at
        } for exp in expenses.items]
    }), 200

@app.route('/api/expenses/<int:exp_id>', methods=['GET'])
@jwt_required()
def get_expense(exp_id):
    expense = ExpenseReport.query.get(exp_id)
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    return jsonify({
        'id': expense.id,
        'title': expense.title,
        'amount': float(expense.amount),
        'date': expense.date,
        'description': expense.description,
        'status': expense.status,
        'category_id': expense.category_id,
        'attachments': [{
            'id': att.id,
            'filename': att.filename,
            'url': f'/api/attachments/{att.id}'
        } for att in expense.attachments],
        'created_at': expense.created_at
    }), 200

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title') or not data.get('amount'):
        return jsonify({'error': 'Title and amount are required'}), 400
    
    expense = ExpenseReport(
        title=data['title'],
        amount=data['amount'],
        description=data.get('description'),
        status=data.get('status', 'draft'),
        category_id=data.get('category_id'),
        created_by=user_id
    )
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({
        'id': expense.id,
        'title': expense.title,
        'amount': float(expense.amount),
        'status': expense.status,
        'created_at': expense.created_at
    }), 201

@app.route('/api/expenses/<int:exp_id>', methods=['PUT'])
@jwt_required()
def update_expense(exp_id):
    expense = ExpenseReport.query.get(exp_id)
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    data = request.get_json()
    
    expense.title = data.get('title', expense.title)
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    expense.status = data.get('status', expense.status)
    expense.category_id = data.get('category_id', expense.category_id)
    
    db.session.commit()
    
    return jsonify({
        'id': expense.id,
        'title': expense.title,
        'amount': float(expense.amount),
        'status': expense.status,
        'updated_at': expense.created_at
    }), 200

@app.route('/api/expenses/<int:exp_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(exp_id):
    expense = ExpenseReport.query.get(exp_id)
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    # Delete attachments
    for attachment in expense.attachments:
        if os.path.exists(attachment.filepath):
            os.remove(attachment.filepath)
        db.session.delete(attachment)
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted successfully'}), 200

# ==================== File Upload Endpoints ====================

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/expenses/<int:exp_id>/upload', methods=['POST'])
@jwt_required()
def upload_attachment(exp_id):
    expense = ExpenseReport.query.get(exp_id)
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    attachment = Attachment(
        filename=file.filename,
        filepath=filepath,
        mimetype=file.content_type,
        expense_id=exp_id
    )
    
    db.session.add(attachment)
    db.session.commit()
    
    return jsonify({
        'id': attachment.id,
        'filename': attachment.filename,
        'url': f'/api/attachments/{attachment.id}',
        'uploaded_at': attachment.uploaded_at
    }), 201

@app.route('/api/attachments/<int:att_id>', methods=['GET'])
def download_attachment(att_id):
    attachment = Attachment.query.get(att_id)
    
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    
    if not os.path.exists(attachment.filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(
        os.path.dirname(attachment.filepath),
        os.path.basename(attachment.filepath),
        as_attachment=True,
        download_name=attachment.filename
    )

@app.route('/api/attachments/<int:att_id>', methods=['DELETE'])
@jwt_required()
def delete_attachment(att_id):
    attachment = Attachment.query.get(att_id)
    
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    
    if os.path.exists(attachment.filepath):
        os.remove(attachment.filepath)
    
    db.session.delete(attachment)
    db.session.commit()
    
    return jsonify({'message': 'Attachment deleted successfully'}), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-expense'}), 200

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
