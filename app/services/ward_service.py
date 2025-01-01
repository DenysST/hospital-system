from app.config import SingletonMeta
from app.repositories import WardRepository
from app.repositories import DepartmentRepository
from app.models import Ward


class WardService(metaclass=SingletonMeta):
    def __init__(self):
        self._ward_repository = WardRepository()
        self._department_repository = DepartmentRepository()

    def add_ward(self, number: int, bed_capacity: int, department_id: int):
        department = self._department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department does not exist.")

        if self._ward_repository.get_by_number(number):
            raise ValueError("Ward number must be unique.")

        if bed_capacity <= 0:
            raise ValueError("Ward capacity must be a positive integer.")

        ward = Ward(number=number, bed_capacity=bed_capacity, department_id=department_id)
        return self._ward_repository.add(ward)

    def update_ward(self, ward_id: int, number: int = None, bed_capacity: int = None, department_id: int = None):
        ward = self._ward_repository.get_by_id(ward_id)
        if not ward:
            raise ValueError("Ward not found.")

        if department_id is not None:
            department = self._department_repository.get_by_id(department_id)
            if not department:
                raise ValueError("Department does not exist.")

        if number is not None and ward.number != number and self._ward_repository.get_by_number(number):
            raise ValueError("Ward number must be unique.")

        if bed_capacity is not None and bed_capacity <= 0:
            raise ValueError("Ward capacity must be a positive integer.")

        ward.number = number
        ward.bed_capacity = bed_capacity
        ward.department_id = department_id

        return self._ward_repository.update(ward)

    def get_all_wards(self):
        return self._ward_repository.get_all()

    def get_ward_by_id(self, ward_id: int):
        ward = self._ward_repository.get_by_id(ward_id)
        if not ward:
            raise ValueError("Ward not found.")
        return ward
