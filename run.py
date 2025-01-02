from app import create_app
from app.repositories import DepartmentRepository
from app.repositories import WardRepository
from app.repositories import DoctorRepository
from app.repositories import PatientRepository
from app.services.department_service import DepartmentService

from flask_injector import FlaskInjector
from sqlalchemy.orm import scoped_session, Session

from app import db

app = create_app()

# # Configure DI
# def configure(binder):
#     session_factory = scoped_session(db.session)
#
#     # Bind SQLAlchemy sessions
#     binder.bind(Session, to=session_factory)
#
#     # Bind repositories
#     binder.bind(DepartmentRepository, to=lambda: DepartmentRepository(session_factory()), scope=Session)
#     binder.bind(WardRepository, to=lambda: WardRepository(session_factory()), scope=Session)
#     binder.bind(DoctorRepository, to=lambda: DoctorRepository(session_factory()), scope=Session)
#     binder.bind(PatientRepository, to=lambda: PatientRepository(session_factory()), scope=Session)
#
#     # Bind services
#     binder.bind(DepartmentService, to=lambda: DepartmentService(DepartmentRepository(session_factory())), scope=Session)
#     # binder.bind(WardService, to=lambda: WardService(WardRepository(session_factory()), DepartmentRepository(session_factory())), scope=Session)
#     # binder.bind(DoctorService, to=lambda: DoctorService(DoctorRepository(session_factory())), scope=Session)
#     # binder.bind(PatientService, to=lambda: PatientService(PatientRepository(session_factory()), WardRepository(session_factory()), DoctorRepository(session_factory())), scope=Session)
#
# FlaskInjector(app=app, modules=[configure])

if __name__ == "__main__":
    app.run(port=5001)