from .users import users_bp
from .services import services_bp
from .appointments import appointments_bp
from .availability import availability_bp

def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(availability_bp)
