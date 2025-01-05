import pytest
from app.models import Doctor, Department
from app.services.doctor_service import DoctorService
from app.repositories import DoctorRepository
from app.repositories import DepartmentRepository


@pytest.fixture
def mock_doctor_repository(mocker):
    return mocker.create_autospec(DoctorRepository)


@pytest.fixture
def mock_department_repository(mocker):
    return mocker.create_autospec(DepartmentRepository)


@pytest.fixture
def service(mock_doctor_repository, mock_department_repository):
    return DoctorService(mock_doctor_repository, mock_department_repository)


def test_add_doctor_success(service, mock_doctor_repository, mock_department_repository):
    mock_department_repository.get_by_id.return_value = Department(id=1, name="Cardiology")
    mock_doctor_repository.add.return_value = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=1)

    doctor = service.add_doctor("Dr. Smith", "Cardiologist", 1)

    assert doctor.id == 1
    assert doctor.name == "Dr. Smith"
    assert doctor.specialization == "Cardiologist"
    assert doctor.department_id == 1
    mock_department_repository.get_by_id.assert_called_once_with(1)
    mock_doctor_repository.add.assert_called_once()


def test_add_doctor_department_not_found(service, mock_doctor_repository, mock_department_repository):
    mock_department_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Department does not exist."):
        service.add_doctor("Dr. Smith", "Cardiologist", 999)

    mock_department_repository.get_by_id.assert_called_once_with(999)
    mock_doctor_repository.add.assert_not_called()


def test_update_doctor_success(service, mock_doctor_repository, mock_department_repository):
    mock_doctor_repository.get_by_id.return_value = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=1)
    mock_department_repository.get_by_id.return_value = Department(id=2, name="Neurology")

    service.update_doctor(1, name="Dr. John", specialization="Neurologist", department_id=2)

    mock_doctor_repository.get_by_id.assert_called_once_with(1)
    mock_department_repository.get_by_id.assert_called_once_with(2)
    mock_doctor_repository.update.assert_called_once()


def test_update_doctor_not_found(service, mock_doctor_repository):
    mock_doctor_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Doctor not found."):
        service.update_doctor(1, name="Dr. John")

    mock_doctor_repository.get_by_id.assert_called_once_with(1)
    mock_doctor_repository.update.assert_not_called()


def test_get_doctor_by_id_success(service, mock_doctor_repository):
    mock_doctor_repository.get_by_id.return_value = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=1)

    doctor = service.get_doctor_by_id(1)

    assert doctor.id == 1
    assert doctor.name == "Dr. Smith"
    assert doctor.specialization == "Cardiologist"
    assert doctor.department_id == 1
    mock_doctor_repository.get_by_id.assert_called_once_with(1)


def test_get_doctor_by_id_not_found(service, mock_doctor_repository):
    mock_doctor_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Doctor not found."):
        service.get_doctor_by_id(1)

    mock_doctor_repository.get_by_id.assert_called_once_with(1)


def test_get_doctors_by_department_success(service, mock_doctor_repository, mock_department_repository):
    mock_department_repository.get_by_id.return_value = Department(id=1, name="Cardiology")
    mock_doctor_repository.get_by_department.return_value = [
        Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=1),
        Doctor(id=2, name="Dr. John", specialization="Neurologist", department_id=1),
    ]

    doctors = service.get_doctors_by_department(1)

    assert len(doctors) == 2
    assert doctors[0].name == "Dr. Smith"
    assert doctors[1].name == "Dr. John"
    mock_department_repository.get_by_id.assert_called_once_with(1)
    mock_doctor_repository.get_by_department.assert_called_once_with(1)


def test_get_doctors_by_department_not_found(service, mock_department_repository):
    mock_department_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Department does not exist."):
        service.get_doctors_by_department(999)

    mock_department_repository.get_by_id.assert_called_once_with(999)


def test_get_all_doctors_success(service, mock_doctor_repository):
    mock_doctor_repository.get_all.return_value = [
        Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=1),
        Doctor(id=2, name="Dr. John", specialization="Neurologist", department_id=2),
    ]

    doctors = service.get_all_doctors()

    assert len(doctors) == 2
    assert doctors[0].name == "Dr. Smith"
    assert doctors[1].name == "Dr. John"
    mock_doctor_repository.get_all.assert_called_once()
