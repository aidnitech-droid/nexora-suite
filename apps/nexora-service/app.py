from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import datetime

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nexora_service.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class Technician(db.Model):
    __tablename__ = 'service_technicians'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    skills = db.Column(db.Text)  # comma-separated or JSON in future
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'skills': self.skills,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class JobTicket(db.Model):
    __tablename__ = 'service_job_tickets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    customer_name = db.Column(db.String(255))
    customer_address = db.Column(db.Text)
    scheduled_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(50), default='open')  # open, assigned, in_progress, completed, cancelled
    technician_id = db.Column(db.Integer, db.ForeignKey('service_technicians.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    technician = db.relationship('Technician', backref=db.backref('jobs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'priority': self.priority,
            'status': self.status,
            'technician_id': self.technician_id,
            'technician': self.technician.to_dict() if self.technician else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

with app.app_context():
    db.create_all()

# Role decorator stub (can be extended)
def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            # simple placeholder: in future check user role
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ==================== Module Root ====================

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'module': 'nexora-service',
        'status': 'running',
        'endpoints': ['/api/auth/register', '/api/auth/login', '/api/services', '/api/health']
    }), 200

# Technicians endpoints
@app.route('/api/service/technicians', methods=['GET'])
def list_technicians():
    techs = Technician.query.order_by(Technician.created_at.desc()).all()
    return jsonify([t.to_dict() for t in techs]), 200

@app.route('/api/service/technicians/<int:tech_id>', methods=['GET'])
def get_technician(tech_id):
    t = Technician.query.get_or_404(tech_id)
    return jsonify(t.to_dict()), 200

@app.route('/api/service/technicians', methods=['POST'])
def create_technician():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400
    t = Technician(name=data['name'], phone=data.get('phone'), email=data.get('email'), skills=data.get('skills'))
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@app.route('/api/service/technicians/<int:tech_id>', methods=['PUT'])
def update_technician(tech_id):
    t = Technician.query.get_or_404(tech_id)
    data = request.get_json() or {}
    t.name = data.get('name', t.name)
    t.phone = data.get('phone', t.phone)
    t.email = data.get('email', t.email)
    t.skills = data.get('skills', t.skills)
    t.active = data.get('active', t.active)
    db.session.commit()
    return jsonify(t.to_dict()), 200

@app.route('/api/service/technicians/<int:tech_id>', methods=['DELETE'])
def delete_technician(tech_id):
    t = Technician.query.get_or_404(tech_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'technician deleted'}), 200

# Job tickets endpoints
@app.route('/api/service/jobs', methods=['GET'])
def list_jobs():
    # support filtering by status and technician_id
    status = request.args.get('status')
    tech = request.args.get('technician_id', type=int)
    q = JobTicket.query
    if status:
        q = q.filter(JobTicket.status == status)
    if tech:
        q = q.filter(JobTicket.technician_id == tech)
    jobs = q.order_by(JobTicket.created_at.desc()).all()
    return jsonify([j.to_dict() for j in jobs]), 200

@app.route('/api/service/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    j = JobTicket.query.get_or_404(job_id)
    return jsonify(j.to_dict()), 200

@app.route('/api/service/jobs', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title required'}), 400
    sched = None
    if data.get('scheduled_date'):
        try:
            sched = datetime.fromisoformat(data.get('scheduled_date'))
        except Exception:
            sched = None
    j = JobTicket(
        title=data['title'],
        description=data.get('description'),
        customer_name=data.get('customer_name'),
        customer_address=data.get('customer_address'),
        scheduled_date=sched,
        priority=data.get('priority','medium')
    )
    db.session.add(j)
    db.session.commit()
    return jsonify(j.to_dict()), 201

@app.route('/api/service/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    j = JobTicket.query.get_or_404(job_id)
    data = request.get_json() or {}
    j.title = data.get('title', j.title)
    j.description = data.get('description', j.description)
    j.customer_name = data.get('customer_name', j.customer_name)
    j.customer_address = data.get('customer_address', j.customer_address)
    if data.get('scheduled_date'):
        try:
            j.scheduled_date = datetime.fromisoformat(data.get('scheduled_date'))
        except Exception:
            pass
    j.priority = data.get('priority', j.priority)
    # allow status update through this route
    if data.get('status'):
        j.status = data.get('status')
    db.session.commit()
    return jsonify(j.to_dict()), 200

@app.route('/api/service/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    j = JobTicket.query.get_or_404(job_id)
    db.session.delete(j)
    db.session.commit()
    return jsonify({'message': 'job deleted'}), 200

# Assignment endpoint
@app.route('/api/service/jobs/<int:job_id>/assign', methods=['POST'])
def assign_technician(job_id):
    j = JobTicket.query.get_or_404(job_id)
    data = request.get_json() or {}
    tech_id = data.get('technician_id')
    if not tech_id:
        return jsonify({'error': 'technician_id required'}), 400
    tech = Technician.query.get(tech_id)
    if not tech:
        return jsonify({'error': 'technician not found'}), 404
    j.technician_id = tech_id
    j.status = data.get('status', 'assigned')
    db.session.commit()
    return jsonify(j.to_dict()), 200

# Status update endpoint (small route for quick status changes)
@app.route('/api/service/jobs/<int:job_id>/status', methods=['POST'])
def update_job_status(job_id):
    j = JobTicket.query.get_or_404(job_id)
    data = request.get_json() or {}
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'status required'}), 400
    j.status = new_status
    db.session.commit()
    return jsonify(j.to_dict()), 200

# Simple analytics: counts by status and assigned per technician
@app.route('/api/service/analytics', methods=['GET'])
def service_analytics():
    total = JobTicket.query.count()
    by_status = db.session.query(JobTicket.status, db.func.count(JobTicket.id)).group_by(JobTicket.status).all()
    assignments = db.session.query(Technician.id, Technician.name, db.func.count(JobTicket.id)).join(JobTicket, JobTicket.technician_id == Technician.id, isouter=True).group_by(Technician.id).all()
    return jsonify({
        'total_jobs': total,
        'by_status': [{'status': s, 'count': c} for s,c in by_status],
        'assignments': [{'technician_id': tid, 'name': name, 'count': cnt} for tid, name, cnt in assignments]
    }), 200

# Health
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'nexora-service'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5030)
