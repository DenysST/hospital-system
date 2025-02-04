import pytest
from unittest.mock import MagicMock
from app.models import Department, Ward
from app.services.department_service import DepartmentService
from app.repositories import DepartmentRepository


@pytest.fixture
def mock_repository(mocker):
    return mocker.create_autospec(DepartmentRepository)


@pytest.fixture
def service(mock_repository):
    return DepartmentService(mock_repository)


def test_add_department_success(service, mock_repository):
    mock_repository.get_by_name.return_value = None
    mock_repository.add.return_value = Department(id=1, name="Cardiology")

    department = service.add_department("Cardiology")

    assert department.id == 1
    assert department.name == "Cardiology"
    mock_repository.get_by_name.assert_called_once_with("Cardiology")
    mock_repository.add.assert_called_once()


def test_add_department_duplicate_name(service, mock_repository):
    mock_repository.get_by_name.return_value = Department(id=1, name="Cardiology")

    with pytest.raises(ValueError, match="Department name must be unique."):
        service.add_department("Cardiology")

    mock_repository.get_by_name.assert_called_once_with("Cardiology")
    mock_repository.add.assert_not_called()


def test_update_department_success(service, mock_repository):
    mock_repository.get_by_name.return_value = None
    mock_repository.get_by_id.return_value = Department(id=1, name="Old Name")
    mock_repository.update.return_value = Department(id=1, name="New Name")

    department = service.update_department(1, "New Name")

    assert department.id == 1
    assert department.name == "New Name"
    mock_repository.get_by_name.assert_called_once_with("New Name")
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once()


def test_update_department_not_found(service, mock_repository):
    mock_repository.get_by_name.return_value = None
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Department not found."):
        service.update_department(1, "New Name")

    mock_repository.get_by_name.assert_called_once_with("New Name")
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_not_called()


def test_get_all_departments(service, mock_repository):
    mock_repository.get_all.return_value = [
        Department(id=1, name="Cardiology"),
        Department(id=2, name="Neurology"),
    ]

    departments = service.get_all_departments()

    assert len(departments) == 2
    assert departments[0].name == "Cardiology"
    assert departments[1].name == "Neurology"
    mock_repository.get_all.assert_called_once()


def test_get_department_by_id_success(service, mock_repository):
    mock_repository.get_by_id.return_value = Department(id=1, name="Cardiology")

    department = service.get_department_by_id(1)

    assert department.id == 1
    assert department.name == "Cardiology"
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_department_by_id_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Department not found."):
        service.get_department_by_id(1)

    mock_repository.get_by_id.assert_called_once_with(1)


def test_calculate_bed_occupancy(service, mock_repository):
    ward1 = Ward(bed_capacity=10, patients=[MagicMock()] * 7)
    ward2 = Ward(bed_capacity=5, patients=[MagicMock()] * 3)
    department = Department(id=1, name="Cardiology", wards=[ward1, ward2])

    mock_repository.get_all_with_relations.return_value = [department]

    occupancy_data = service.calculate_bed_occupancy()

    assert len(occupancy_data) == 1
    assert occupancy_data[0]['department_id'] == 1
    assert occupancy_data[0]['department_name'] == "Cardiology"
    assert occupancy_data[0]['total_beds'] == 15
    assert occupancy_data[0]['occupied_beds'] == 10
    assert occupancy_data[0]["occupancy_percentage"] == 66.67
    mock_repository.get_all_with_relations.assert_called_once()