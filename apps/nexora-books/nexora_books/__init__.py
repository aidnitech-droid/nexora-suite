from flask import Blueprint

nexora_books_bp = Blueprint('nexora_books', __name__, template_folder='templates', static_folder='static')

from . import routes, api  # noqa: E402,F401
