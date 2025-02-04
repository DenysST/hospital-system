from app.models import Department, DepartmentOccupancySchema
from app.repositories import DepartmentRepository


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository):
        self._repository = department_repository

    def add_department(self, name: str):
        if self._repository.get_by_name(name):
            raise ValueError("Department name must be unique.")
        department = Department(name=name)
        return self._repository.add(department)

    def update_department(self, department_id: int, name: str):
        existing = self._repository.get_by_name(name)
        if existing and existing.id != department_id:
            raise ValueError("Department name must be unique.")
        department = self._repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")
        department.name = name
        return self._repository.update(department)

    def get_all_departments(self, with_relations=False):
        if with_relations:
            return self._repository.get_all_with_relations()
        return self._repository.get_all()

    def get_department_by_id(self, department_id: int, with_relations=False):
        if with_relations:
            department = self._repository.get_by_id_with_relations(department_id)
        else:
            department = self._repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")
        return department

    def calculate_bed_occupancy(self):
        departments = self._repository.get_all_with_relations()
        occupancy_data = []

        for department in departments:
            total_beds = sum(ward.bed_capacity for ward in department.wards)
            occupied_beds = sum(len(ward.patients) for ward in department.wards)
            occupancy_percentage = (occupied_beds / total_beds * 100) if total_beds > 0 else 0
            occupancy_data.append(
                DepartmentOccupancySchema().load({
                    "department_id": department.id,
                    "department_name": department.name,
                    "total_beds": total_beds,
                    "occupied_beds": occupied_beds,
                    "occupancy_percentage": round(occupancy_percentage, 2)
                })
            )

        return occupancy_data