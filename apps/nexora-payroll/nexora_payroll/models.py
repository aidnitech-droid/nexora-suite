from datetime import datetime
from app import db


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True)
    hire_date = db.Column(db.Date, default=datetime.utcnow)
    salary_structure_id = db.Column(db.Integer, db.ForeignKey('salary_structures.id'))

    attendance = db.relationship('Attendance', backref='employee', lazy=True)
    payslips = db.relationship('Payslip', backref='employee', lazy=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'salary_structure_id': self.salary_structure_id
        }


class SalaryStructure(db.Model):
    __tablename__ = 'salary_structures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    base_salary = db.Column(db.Float, default=0.0)
    allowances = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)

    employees = db.relationship('Employee', backref='salary_structure', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'base_salary': self.base_salary,
            'allowances': self.allowances,
            'deductions': self.deductions
        }


class Payslip(db.Model):
    __tablename__ = 'payslips'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    gross = db.Column(db.Float)
    net = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'gross': self.gross,
            'net': self.net,
            'created_at': self.created_at.isoformat()
        }


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date)
    status = db.Column(db.String(50))  # present, absent, leave
    hours = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status,
            'hours': self.hours
        }
