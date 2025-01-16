import os
from app.consts import MESSAGE
from app.extentions import db, migrate
from app.di_container import ApplicationContainer
from flask_smorest import Api


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
        API_TITLE="Hospital API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_JSON_PATH="openapi.json",
        OPENAPI_SWAGGER_UI_PATH="/swagger-ui",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    )

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    from app.views.department_view import bp as department_bp
    from app.views.ward_view import bp as ward_bp
    from app.views.doctor_view import bp as doctor_bp
    from app.views.patients_view import bp as patient_bp
    api.register_blueprint(department_bp)
    api.register_blueprint(ward_bp)
    api.register_blueprint(doctor_bp)
    api.register_blueprint(patient_bp)

    with app.app_context():
        from app.models import models

    return app
