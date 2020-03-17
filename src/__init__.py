from flask import Flask

from src.personal_web import personal_bp


def create_app():
    """Creates the app with Blueprints registered"""
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(personal_bp)
