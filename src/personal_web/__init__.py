"""Main module of the application"""

from flask import Blueprint

personal_bp = Blueprint('personal_web', __name__, template_folder='templates')

from . import routes
