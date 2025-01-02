from sqlalchemy.orm import joinedload
from app.models import Department, Ward, Doctor, Patient
from app import db
from app.config import SingletonMeta


class BaseRepository(metaclass=SingletonMeta):
    model = None

    def __init__(self):
        self.session = db.session

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, id_):
        return self.session.query(self.model).filter_by(id=id_).first()

    def add(self, instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, instance):
        self.session.commit()
        return instance

    def delete(self, instance):
        self.session.delete(instance)
        self.session.commit()


class DepartmentRepository(BaseRepository):
    model = Department

    def get_by_name(self, name):
        return self.session.query(Department).filter_by(name=name).first()

    def get_all_with_relations(self):
        return (
            self.session.query(Department)
            .options(
                joinedload(Department.wards),
                joinedload(Department.doctors))
            .all())

    def get_by_id_with_relations(self, id_):
        return (
            self.session.query(Department)
            .options(
                joinedload(Department.wards),
                joinedload(Department.doctors))
            .filter_by(id=id_)
            .first())


class WardRepository(BaseRepository):
    model = Ward

    def get_by_number(self, number: int):
        return self.session.query(self.model).filter_by(number=number).first()

    def get_all_with_relations(self):
        return (
            self.session.query(Ward)
            .options(
                joinedload(Ward.department),
                joinedload(Ward.patients))
            .all())


class DoctorRepository(BaseRepository):
    model = Doctor

    def get_by_specialization(self, specialization: str):
        return self.session.query(self.model).filter_by(specialization=specialization).all()

    def get_by_department(self, department_id: int):
        return self.session.query(self.model).filter_by(department_id=department_id).all()


class PatientRepository(BaseRepository):
    model = Patient

    def get_by_ward(self, ward_id: int):
        return self.session.query(self.model).filter_by(ward_id=ward_id).all()

    def get_by_doctor(self, doctor_id: int):
        return self.session.query(self.model).filter_by(doctor_id=doctor_id).all()
