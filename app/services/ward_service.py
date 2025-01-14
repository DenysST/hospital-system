from app.repositories import WardRepository
from app.repositories import DepartmentRepository
from app.models import Ward


class WardService:
    def __init__(self, ward_repository: WardRepository, department_repository: DepartmentRepository):
        self._ward_repository = ward_repository
        self._department_repository = department_repository

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

    def get_wards_by_department(self, department_id: int):
        """
        Retrieve all wards for a given department.
        """
        department = self._department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")

        return self._ward_repository.get_by_id(department_id)

    def calculate_occupancy_percentage(self, ward_id: int) -> float:
        """
        Calculate the occupancy percentage of a ward.
        """
        ward = self._ward_repository.get_by_id(ward_id)
        if not ward:
            raise ValueError("Ward not found.")

        if ward.total_beds == 0:
            return 0.0

        return (ward.occupied_beds / ward.total_beds) * 100

    def summarize_wards(self, department_id: int) -> dict:
        """
        Summarize ward data for a department.
        """
        department = self._department_repository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found.")

        wards = self._ward_repository.get_by_id(department_id)
        return {
            "total_wards": len(wards),
            "total_beds": sum(ward.total_beds for ward in wards),
            "total_occupied": sum(ward.occupied_beds for ward in wards),
            "average_occupancy": (
                sum(ward.occupied_beds for ward in wards) / sum(ward.total_beds for ward in wards)
                if wards else 0.0
            ),
        }

    def delete_ward(self, ward_id: int):
        """
        Delete a ward and handle errors.
        """
        try:
            ward = self._ward_repository.get_by_id(ward_id)
            if not ward:
                raise ValueError("Ward not found.")

            self._ward_repository.delete(ward)
        except ValueError as e:
            print(f"Error deleting ward: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
