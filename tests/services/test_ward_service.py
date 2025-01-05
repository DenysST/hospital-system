import pytest
from app.models import Ward, Department
from app.services.ward_service import WardService
from app.repositories import WardRepository
from app.repositories import DepartmentRepository

@pytest.fixture
def mock_ward_repository(mocker):
    return mocker.create_autospec(WardRepository)

@pytest.fixture
def mock_department_repository(mocker):
    return mocker.create_autospec(DepartmentRepository)

@pytest.fixture
def service(mock_ward_repository, mock_department_repository):
    return WardService(mock_ward_repository, mock_department_repository)

def test_add_ward_success(service, mock_ward_repository, mock_department_repository):
    mock_department_repository.get_by_id.return_value = Department(id=1, name="Cardiology")
    mock_ward_repository.add.return_value = Ward(id=1, number=101, bed_capacity=20, department_id=1)
    mock_ward_repository.get_by_number.return_value = None

    ward = service.add_ward(101, 20, 1)

    assert ward.id == 1
    assert ward.number == 101
    assert ward.bed_capacity == 20
    assert ward.department_id == 1
    mock_department_repository.get_by_id.assert_called_once_with(1)
    mock_ward_repository.add.assert_called_once()

def test_add_ward_department_not_found(service, mock_department_repository):
    mock_department_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Department does not exist."):
        service.add_ward(101, 20, 999)

    mock_department_repository.get_by_id.assert_called_once_with(999)

def test_update_ward_success(service, mock_ward_repository, mock_department_repository):
    mock_ward_repository.get_by_id.return_value = Ward(id=1, number=101, bed_capacity=20, department_id=1)
    mock_department_repository.get_by_id.return_value = Department(id=2, name="Neurology")
    mock_ward_repository.update.return_value = Ward(id=1, number=101, bed_capacity=25, department_id=2)

    ward = service.update_ward(1, bed_capacity=25, department_id=2)

    assert ward.bed_capacity == 25
    assert ward.department_id == 2
    mock_ward_repository.get_by_id.assert_called_once_with(1)
    mock_department_repository.get_by_id.assert_called_once_with(2)
    mock_ward_repository.update.assert_called_once()

def test_update_ward_not_found(service, mock_ward_repository):
    mock_ward_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Ward not found."):
        service.update_ward(999, bed_capacity=25)

    mock_ward_repository.get_by_id.assert_called_once_with(999)

def test_get_ward_by_id_success(service, mock_ward_repository):
    mock_ward_repository.get_by_id.return_value = Ward(id=1, number=101, bed_capacity=20, department_id=1)

    ward = service.get_ward_by_id(1)

    assert ward.id == 1
    assert ward.number == 101
    assert ward.bed_capacity == 20
    assert ward.department_id == 1
    mock_ward_repository.get_by_id.assert_called_once_with(1)

def test_get_ward_by_id_not_found(service, mock_ward_repository):
    mock_ward_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Ward not found."):
        service.get_ward_by_id(999)

    mock_ward_repository.get_by_id.assert_called_once_with(999)

def test_get_all_wards_success(service, mock_ward_repository):
    mock_ward_repository.get_all.return_value = [
        Ward(id=1, number=101, bed_capacity=20, department_id=1),
        Ward(id=2, number=102, bed_capacity=15, department_id=2),
    ]

    wards = service.get_all_wards()

    assert len(wards) == 2
    assert wards[0].number == 101
    assert wards[1].number == 102
    mock_ward_repository.get_all.assert_called_once()