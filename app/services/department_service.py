from app.config import SingletonMeta
from app.models import Department
from app.repositories import DepartmentRepository


class DepartmentService(metaclass=SingletonMeta):
    def __init__(self):
        self.repository = DepartmentRepository()

    def add_department(self, name: str):
        if self.repository.get_by_name(name):
            raise ValueError("Department name must be unique.")
        department = Department(name=name)
        return self.repository.add(department)

    def update_department(self, department_id: int, name: str):
        existing = self.repository.get_by_name(name)
        if existing and existing.id != department_id:
            raise ValueError("Department name must be unique.")
        department = self.repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")
        department.name = name
        return self.repository.update(department)

    def get_all_departments(self):
        return self.repository.get_all()

    def get_department_by_id(self, department_id: int):
        department = self.repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")
        return department