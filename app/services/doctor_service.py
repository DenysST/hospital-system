from app.models import Doctor
from app.repositories import DoctorRepository
from app.repositories import DepartmentRepository


class DoctorService:
    def __init__(self, doctor_repository: DoctorRepository, department_repository: DepartmentRepository):
        self._doctor_repository = doctor_repository
        self._department_repository = department_repository

    def add_doctor(self, name: str, specialization: str, department_id: int):
        department = self._department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department does not exist.")

        doctor = Doctor(name=name, specialization=specialization, department_id=department_id)
        return self._doctor_repository.add(doctor)

    def update_doctor(self, doctor_id: int, name: str = None, specialization: str = None, department_id: int = None):
        doctor = self._doctor_repository.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found.")

        if department_id is not None:
            department = self._department_repository.get_by_id(department_id)
            if not department:
                raise ValueError("Department does not exist.")

        if name is not None:
            doctor.name = name
        if specialization is not None:
            doctor.specialization = specialization
        if department_id is not None:
            doctor.department_id = department_id

        return self._doctor_repository.update(doctor)

    def get_doctor_by_id(self, doctor_id: int):
        doctor = self._doctor_repository.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found.")
        return doctor

    def get_doctors_by_department(self, department_id: int):
        department = self._department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department does not exist.")

        return self._doctor_repository.get_by_department(department_id)

    def get_all_doctors(self):
        return self._doctor_repository.get_all()