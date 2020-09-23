from .api import api_blueprint

def register_blueprints(app):
    app.register_blueprint(api_blueprint)