# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from datetime import datetime
import os

from flask import Flask, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from app.firebase import Firebase
from app.security import Security


# Instantiate Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
fb = None
sec = None

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Login
    login.init_app(app)

    # Setup Firebase
    fb = Firebase(app)

    # Setup Security
    sec = Security(fb)

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    # Setup Flask-User to handle user account related forms
    from .models.mark_hunter import User

    @app.before_request
    def before_request():
        sec.validate_token(request.headers)

    @app.after_request
    def after_request(response):
        if "Origin" in request.headers:
            response.headers.add('Access-Control-Allow-Origin', request.headers["Origin"])
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


    return app
