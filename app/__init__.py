from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_injector import FlaskInjector
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.views.department_view import bp as department_bp
    from app.views.ward_view import bp as ward_bp
    from app.views.doctor_view import bp as doctor_bp
    app.register_blueprint(department_bp, url_prefix="/api")
    app.register_blueprint(ward_bp, url_prefix="/api")
    app.register_blueprint(doctor_bp, url_prefix="/api")


    with app.app_context():
        from app.models import models

    return app
