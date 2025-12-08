from flask import render_template, request, redirect, url_for, flash
from . import nexora_payroll_bp
from .models import db, Employee, Attendance
from .payroll import PayrollEngine
from datetime import datetime


@nexora_payroll_bp.route('/payroll/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        emp_id = request.form.get('employee_id')
        date_str = request.form.get('date')
        status = request.form.get('status')
        hours = float(request.form.get('hours', 0))
        d = datetime.fromisoformat(date_str).date() if date_str else None
        att = Attendance(employee_id=emp_id, date=d, status=status, hours=hours)
        db.session.add(att)
        db.session.commit()
        flash('Attendance recorded', 'success')
        return redirect(url_for('nexora_payroll.attendance'))
    records = Attendance.query.order_by(Attendance.date.desc()).limit(50).all()
    return render_template('nexora_payroll/attendance.html', records=records)


@nexora_payroll_bp.route('/payroll/generate-payslip', methods=['GET', 'POST'])
def generate_payslip():
    if request.method == 'POST':
        emp_id = int(request.form.get('employee_id'))
        start = request.form.get('period_start')
        end = request.form.get('period_end')
        start_date = datetime.fromisoformat(start).date()
        end_date = datetime.fromisoformat(end).date()
        engine = PayrollEngine()
        payslip = engine.calculate_payslip(emp_id, start_date, end_date)
        return render_template('nexora_payroll/payslip.html', payslip=payslip)
    employees = Employee.query.all()
    return render_template('nexora_payroll/generate_payslip.html', employees=employees)
