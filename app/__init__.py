import os

from app.consts import MESSAGE
from app.di_container import ApplicationContainer
from app.extentions import db, migrate
from app.di_container import ApplicationContainer


def create_app():
    container = ApplicationContainer()
    app = container.app()
    container.wire(modules=[
        "app.views.department_view",
        "app.views.ward_view",
        "app.views.doctor_view",
        "app.views.patients_view",
    ])

    app.container = container
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/hospital_db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "denys.stefanko@gmail.com"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", ""),
        MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER", "denys.stefanko@gmail.com"),
    )
    print(app.config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.views.department_view import bp as department_bp
    from app.views.ward_view import bp as ward_bp
    from app.views.doctor_view import bp as doctor_bp
    from app.views.patients_view import bp as patient_bp
    app.register_blueprint(department_bp, url_prefix="/api")
    app.register_blueprint(ward_bp, url_prefix="/api")
    app.register_blueprint(doctor_bp, url_prefix="/api")
    app.register_blueprint(patient_bp, url_prefix="/api")

    with app.app_context():
        from app.models import models

    return app
