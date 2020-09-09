from .api import api_blueprint
from .login import login_blueprint

def register_blueprints(app):
    app.register_blueprint(api_blueprint)
    app.register_blueprint(login_blueprint)