from flask import Blueprint

nexora_payroll_bp = Blueprint('nexora_payroll', __name__, template_folder='templates', static_folder='static')

from . import routes, api  # noqa: E402,F401
