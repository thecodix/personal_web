"""Application routes"""
from . import personal_bp


@personal_bp.route('/')
def maim_view():
    """Displays hello world"""
    return 'Hello World!'
