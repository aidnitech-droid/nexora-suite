from datetime import date
from .models import SalaryStructure, Payslip, Employee
from app import db


class PayrollEngine:
    """Simple payroll calculation engine."""
    def __init__(self):
        pass

    def calculate_payslip(self, employee_id, period_start, period_end):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValueError('Employee not found')
        ss = employee.salary_structure
        base = ss.base_salary if ss else 0.0
        allowances = ss.allowances if ss else 0.0
        deductions = ss.deductions if ss else 0.0

        gross = base + allowances
        net = gross - deductions

        payslip = Payslip(
            employee_id=employee.id,
            period_start=period_start,
            period_end=period_end,
            gross=gross,
            net=net
        )
        db.session.add(payslip)
        db.session.commit()
        return payslip
