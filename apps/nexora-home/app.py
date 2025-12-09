from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import ast
import os
from datetime import datetime
import sys

# Add parent directory to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))  # parent apps/ directory
COMMON_DIR = os.path.abspath(os.path.join(APPS_DIR, '..', 'common'))
sys.path.insert(0, COMMON_DIR)

from utils.pricing_guard import (
    get_pricing_status,
    get_banner_data,
    apply_pricing_middleware,
    pricing_guard,
    is_free_tier_active,
)

DEMO_MODE = os.getenv('DEMO_MODE', '0').lower() in ('1', 'true', 'yes')

DEMO_CREDENTIALS = {
    'email': 'demo@nexora.com',
    'username': 'demo',
    'password': 'Demo1234',
    'role': 'demo'
}

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'nexora_home.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('NEXORA_HOME_SECRET', 'dev-secret')

db = SQLAlchemy(app)

# Apply pricing middleware to add headers to all responses
apply_pricing_middleware(app)

# Initialization flag to ensure db.create_all() runs only once
_initialized = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return redirect(url_for('login', next=request.path))
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return "Forbidden", 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.before_request
def initialize_and_block_deletes():
    global _initialized
    # Initialize on first request
    if not _initialized:
        db.create_all()
        # Seed demo user when running in demo mode
        if DEMO_MODE:
            demo = User.query.filter((User.username == DEMO_CREDENTIALS['username']) | (User.email == DEMO_CREDENTIALS['email'])).first()
            if not demo:
                demo = User(username=DEMO_CREDENTIALS['username'], email=DEMO_CREDENTIALS['email'], role=DEMO_CREDENTIALS['role'])
                demo.set_password(DEMO_CREDENTIALS['password'])
                db.session.add(demo)
                db.session.commit()
        _initialized = True
    # Block DELETE requests in demo mode
    if DEMO_MODE and request.method == 'DELETE':
        return jsonify({'error': 'DELETE disabled in demo mode'}), 403


@app.context_processor
def inject_demo_flag():
    return {
        'demo_mode': DEMO_MODE,
        'pricing_status': get_pricing_status(),
        'banner_data': get_banner_data(),
        'free_tier_active': is_free_tier_active(),
    }


@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        if not username or not email or not password:
            return render_template('register.html', error='Missing fields')
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return render_template('register.html', error='User exists')
        u = User(username=username, email=email, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        session['user_id'] = u.id
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Accept username or email for login
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            next_url = request.args.get('next') or url_for('dashboard')
            return redirect(next_url)
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    # discover modules (folders under apps/)
    apps_root = APPS_DIR
    modules = []
    try:
        def get_module_description(path):
            # Try README files first
            for fname in ('README.md', 'README.MD', 'README', 'README.txt'):
                fpath = os.path.join(path, fname)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, 'r', encoding='utf-8') as fh:
                            return fh.read()
                    except Exception:
                        break
            # Fallback: try to extract top-level docstring from app.py or __init__.py
            for candidate in ('app.py', '__init__.py'):
                fpath = os.path.join(path, candidate)
                if os.path.exists(fpath):
                    try:
                        src = open(fpath, 'r', encoding='utf-8').read()
                        module = ast.parse(src)
                        doc = ast.get_docstring(module)
                        if doc:
                            return doc
                    except Exception:
                        pass
            return None

        for name in sorted(os.listdir(apps_root)):
            path = os.path.join(apps_root, name)
            if os.path.isdir(path):
                readme = get_module_description(path)
                modules.append({'name': name, 'path': path, 'readme': readme})
    except Exception:
        modules = []
    return render_template('dashboard.html', user=user, modules=modules)


@app.route('/module/<module_name>')
@login_required
def module_detail(module_name):
    apps_root = APPS_DIR
    path = os.path.join(apps_root, module_name)
    if not os.path.isdir(path):
        return "Not found", 404
    # Try to obtain a descriptive README or docstring
    def get_module_description(path):
        for fname in ('README.md', 'README.MD', 'README', 'README.txt'):
            fpath = os.path.join(path, fname)
            if os.path.exists(fpath):
                try:
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        return fh.read()
                except Exception:
                    break
        for candidate in ('app.py', '__init__.py'):
            fpath = os.path.join(path, candidate)
            if os.path.exists(fpath):
                try:
                    src = open(fpath, 'r', encoding='utf-8').read()
                    module = ast.parse(src)
                    doc = ast.get_docstring(module)
                    if doc:
                        return doc
                except Exception:
                    pass
        return None

    readme = get_module_description(path)

    # Try to detect a health endpoint in source files
    suggested_health = None
    for candidate in ('app.py',):
        fpath = os.path.join(path, candidate)
        if os.path.exists(fpath):
            try:
                text = open(fpath, 'r', encoding='utf-8').read()
                if '/api/health' in text or 'def health' in text:
                    suggested_health = f'http://localhost:5000/{module_name}/api/health'
                    break
            except Exception:
                pass

    info = {
        'name': module_name,
        'path': path,
        'readme': readme,
        'suggested_health_url': suggested_health
    }
    return render_template('module.html', module=info)


@app.route('/api/nexora-home/modules', methods=['GET'])
@login_required
def api_modules():
    apps_root = APPS_DIR
    modules = []
    for name in sorted(os.listdir(apps_root)):
        path = os.path.join(apps_root, name)
        if os.path.isdir(path):
            modules.append({'name': name, 'path': path})
    return jsonify({'modules': modules})


# Legal & Compliance Pages
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')


@app.route('/user-agreement')
def user_agreement():
    return render_template('user_agreement.html')


@app.route('/data-processing-agreement')
def dpa():
    return render_template('dpa.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5060'))
    app.run(host='0.0.0.0', port=port)
