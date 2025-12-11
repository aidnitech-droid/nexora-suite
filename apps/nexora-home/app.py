from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import ast
import json
import os
from datetime import datetime
import sys

# Add parent directory to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))  # parent apps/ directory
COMMON_DIR = os.path.abspath(os.path.join(APPS_DIR, '..', 'common'))
sys.path.insert(0, COMMON_DIR)

# Load environment variables from project .env (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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
    
    # Get list of integrated modules with metadata
    modules = get_integrated_modules()
    
    return render_template('dashboard.html', user=user, modules=modules)


def get_integrated_modules():
    """
    Get all integrated modules with their metadata.
    Returns a list of module info dicts with access URLs.
    """
    apps_root = APPS_DIR
    modules = []
    
    # Module descriptions and icons
    module_info = {
        'nexora-assist': {'icon': '🤖', 'description': 'AI Assistant & Support'},
        'nexora-bigin': {'icon': '📊', 'description': 'Business Intelligence'},
        'nexora-billing': {'icon': '💳', 'description': 'Billing & Payments'},
        'nexora-bookings': {'icon': '📅', 'description': 'Appointments & Bookings'},
        'nexora-books': {'icon': '📚', 'description': 'Accounting & Books'},
        'nexora-checkout': {'icon': '🛒', 'description': 'E-commerce Checkout'},
        'nexora-commerce': {'icon': '🏪', 'description': 'Commerce & Sales'},
        'nexora-crm': {'icon': '👥', 'description': 'Customer Relationship'},
        'nexora-desk': {'icon': '🎫', 'description': 'Help Desk & Support'},
        'nexora-expense': {'icon': '💰', 'description': 'Expense Management'},
        'nexora-forms': {'icon': '📝', 'description': 'Form Builder & Surveys'},
        'nexora-fsm': {'icon': '🔄', 'description': 'Field Service Management'},
        'nexora-inventory': {'icon': '📦', 'description': 'Inventory Management'},
        'nexora-invoice': {'icon': '📄', 'description': 'Invoice & Documents'},
        'nexora-lens': {'icon': '🔍', 'description': 'Analytics & Insights'},
        'nexora-payments': {'icon': '💵', 'description': 'Payment Processing'},
        'nexora-payroll': {'icon': '👔', 'description': 'Payroll Management'},
        'nexora-pos': {'icon': '💾', 'description': 'Point of Sale'},
        'nexora-practice': {'icon': '🎯', 'description': 'Practice & Training'},
        'nexora-route': {'icon': '🗺️', 'description': 'Route Planning'},
        'nexora-routeiq': {'icon': '📍', 'description': 'Route Intelligence'},
        'nexora-salesiq': {'icon': '📈', 'description': 'Sales Intelligence'},
        'nexora-service': {'icon': '🔧', 'description': 'Service Management'},
        'nexora-sign': {'icon': '✍️', 'description': 'Digital Signatures'},
    }
    
    try:
        for name in sorted(os.listdir(apps_root)):
            path = os.path.join(apps_root, name)
            if os.path.isdir(path) and name != 'nexora-home':
                # Get module info
                info = module_info.get(name, {'icon': '⚙️', 'description': name.replace('nexora-', '').title()})
                
                # Get health endpoint URL
                health_url = f"/module/{name}/api/health"
                
                modules.append({
                    'name': name,
                    'display_name': name.replace('nexora-', '').replace('-', ' ').title(),
                    'icon': info['icon'],
                    'description': info['description'],
                    'health_url': health_url,
                    'access_url': f"/module/{name}/"
                })
    except Exception as e:
        print(f"Error loading modules: {e}")
    
    return modules


@app.route('/module/<module_name>')
@login_required
def module_detail(module_name):
    # Redirect to the actual module served by the dispatcher
    # The module is mounted at /<module_name>/ by wsgi.py DispatcherMiddleware
    return redirect(f'/{module_name}/')


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


# ==================== Module Integration ====================
# Load and integrate all module routes as sub-features

def register_module_routes():
    """
    Dynamically register routes from all modules.
    
    Each module (billing, crm, etc.) has API routes that are registered
    under /module/<module-name>/ prefix.
    
    This allows all modules to run as part of the single home app while
    maintaining separate code organization and independent updates.
    """
    import importlib.util
    from pathlib import Path
    
    base_dir = os.path.dirname(__file__)
    apps_dir = os.path.join(base_dir, '..')
    
    registered_count = 0
    errors = []
    
    # Iterate through all module directories
    for module_dir in sorted(Path(apps_dir).iterdir()):
        if not module_dir.is_dir() or module_dir.name == 'nexora-home':
            continue
        
        app_py_path = module_dir / 'app.py'
        if not app_py_path.exists():
            continue
        
        module_name = module_dir.name
        
        try:
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(
                f"nexora_module_{module_name}",
                str(app_py_path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the Flask app from the module
            module_app = getattr(module, 'app', None)
            if not module_app:
                continue

            # If the module has a frontend folder, serve its index.html at
            # /module/<name>/ and static/assets under /module/<name>/static/ or /module/<name>/assets/
            frontend_dir = os.path.join(str(module_dir), 'frontend')
            served_frontend = False
            if os.path.isdir(frontend_dir):
                # Prefer a built 'dist' directory when present
                dist_dir = os.path.join(frontend_dir, 'dist') if os.path.isdir(os.path.join(frontend_dir, 'dist')) else frontend_dir
                index_html = os.path.join(dist_dir, 'index.html')
                if os.path.exists(index_html):
                    from flask import send_from_directory

                    def make_index_handler(dpath):
                        @login_required
                        def index_handler():
                            return send_from_directory(dpath, 'index.html')
                        return index_handler

                    app.add_url_rule(f"/module/{module_name}/", endpoint=f"{module_name}_frontend_index", view_func=make_index_handler(dist_dir), methods=['GET'])

                    def make_static_handler(dpath):
                        def static_handler(filename):
                            return send_from_directory(dpath, filename)
                        return static_handler

                    app.add_url_rule(f"/module/{module_name}/static/<path:filename>", endpoint=f"{module_name}_frontend_static", view_func=make_static_handler(dist_dir), methods=['GET'])
                    app.add_url_rule(f"/module/{module_name}/assets/<path:filename>", endpoint=f"{module_name}_frontend_assets", view_func=make_static_handler(dist_dir), methods=['GET'])
                    served_frontend = True

            # Extract and register routes from module app
            for rule in list(module_app.url_map.iter_rules()):
                if rule.endpoint in ('static', 'debug.static'):
                    continue
                
                # Include root route so module root is available at
                # /module/<module_name>/ (map module's '/' to that path)
                # (no longer skipping rule '/')
                
                # Create new route in main app with /module/<name> prefix
                new_path = f"/module/{module_name}{rule.rule}"
                
                # Get the view function from module app
                view_func = module_app.view_functions.get(rule.endpoint)
                if not view_func:
                    continue
                
                # Register in main app
                for method in rule.methods - {'HEAD', 'OPTIONS'}:
                    # If the rule is root ('/'), and a frontend is being served,
                    # skip registering the module's own '/' to avoid duplicate handlers.
                    register_path = new_path
                    if rule.rule == '/':
                        register_path = f"/module/{module_name}/"
                        if served_frontend:
                            # frontend index will handle the root path
                            continue

                    app.add_url_rule(
                        register_path,
                        endpoint=f"{module_name}_{rule.endpoint}",
                        view_func=view_func,
                        methods=[method]
                    )
                
                registered_count += 1
            
        except Exception as e:
            errors.append(f"Module {module_name}: {str(e)}")
    
    # Log results
    if registered_count > 0:
        print(f"✓ Registered {registered_count} routes from module apps")
    if errors:
        print(f"⚠ Integration warnings:")
        for err in errors[:3]:  # Show first 3 errors
            print(f"  - {err}")

# Try to register module routes on app startup
try:
    register_module_routes()
except Exception as e:
    print(f"Warning: Module integration failed: {e}")


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5060'))
    app.run(host='0.0.0.0', port=port)
