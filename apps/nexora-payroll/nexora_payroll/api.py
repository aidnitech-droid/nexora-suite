from flask import jsonify, request
from . import nexora_payroll_bp
from .models import db, Employee, SalaryStructure, Payslip, Attendance
from .payroll import PayrollEngine


@nexora_payroll_bp.route('/api/payroll/employees', methods=['GET'])
def api_list_employees():
    emps = Employee.query.all()
    return jsonify([e.to_dict() for e in emps]), 200


@nexora_payroll_bp.route('/api/payroll/employees', methods=['POST'])
def api_create_employee():
    data = request.get_json() or {}
    emp = Employee(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        salary_structure_id=data.get('salary_structure_id')
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201


@nexora_payroll_bp.route('/api/payroll/payslip', methods=['POST'])
def api_generate_payslip():
    data = request.get_json() or {}
    emp_id = data.get('employee_id')
    start = data.get('period_start')
    end = data.get('period_end')
    engine = PayrollEngine()
    payslip = engine.calculate_payslip(emp_id, start, end)
    return jsonify(payslip.to_dict()), 201


@nexora_payroll_bp.route('/api/payroll/attendance', methods=['POST'])
def api_record_attendance():
    data = request.get_json() or {}
    att = Attendance(
        employee_id=data.get('employee_id'),
        date=data.get('date'),
        status=data.get('status'),
        hours=data.get('hours', 0)
    )
    db.session.add(att)
    db.session.commit()
    return jsonify(att.to_dict()), 201
