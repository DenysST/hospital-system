import pytest
from unittest.mock import MagicMock
from app.models import Department, Ward, Doctor, Patient
from app.repositories import DepartmentRepository, WardRepository, DoctorRepository, PatientRepository


@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def department_repository(mock_session):
    department_repo = DepartmentRepository()
    department_repo._session = mock_session
    return department_repo

@pytest.fixture
def ward_repository(mock_session):
    ward_repository = WardRepository()
    ward_repository._session = mock_session
    return ward_repository

@pytest.fixture
def doctor_repository(mock_session):
    doctor_repository = DoctorRepository()
    doctor_repository._session = mock_session
    return doctor_repository

@pytest.fixture
def patient_repository(mock_session):
    patient_repository = PatientRepository()
    patient_repository._session = mock_session
    return patient_repository

def test_base_repository_get_all(department_repository: DepartmentRepository, mock_session):
    departments = [
        Department(id=1, name="Cardiology"),
        Department(id=2, name="Neurology"),
    ]
    mock_session.query().all.return_value = departments

    result = department_repository.get_all()

    assert result == departments
    mock_session.query.assert_called_with(Department)

def test_base_repository_get_by_id(department_repository: DepartmentRepository, mock_session):
    department = Department(id=1, name="Cardiology")
    mock_session.query().filter_by().first.return_value = department

    result = department_repository.get_by_id(1)

    assert result == department
    mock_session.query.assert_called_with(Department)
    mock_session.query().filter_by.assert_called_with(id=1)
    mock_session.query().filter_by().first.assert_called()

def test_base_repository_add(department_repository: DepartmentRepository, mock_session):
    department = Department(name="Cardiology")

    result = department_repository.add(department)

    assert result == department
    mock_session.add.assert_called_with(department)
    mock_session.commit.assert_called()

def test_base_repository_update(department_repository: DepartmentRepository, mock_session):
    department = Department(id=1, name="Cardiology")

    result = department_repository.update(department)

    assert result == department
    mock_session.commit.assert_called()

def test_base_repository_delete(department_repository: DepartmentRepository, mock_session):
    department = Department(id=1, name="Cardiology")

    department_repository.delete(department)

    mock_session.delete.assert_called_with(department)
    mock_session.commit.assert_called()

def test_department_repository_get_by_name(department_repository: DepartmentRepository, mock_session):
    department = Department(id=1, name="Cardiology")
    mock_session.query().filter_by().first.return_value = department

    result = department_repository.get_by_name("Cardiology")

    assert result == department
    mock_session.query.assert_called_with(Department)
    mock_session.query().filter_by.assert_called_with(name="Cardiology")
    mock_session.query().filter_by().first.assert_called()

def test_department_repository_get_all_with_relations(department_repository: DepartmentRepository, mock_session):
    departments = [
        Department(id=1, name="Cardiology"),
        Department(id=2, name="Neurology"),
    ]
    mock_session.query().options().all.return_value = departments

    result = department_repository.get_all_with_relations()

    assert result == departments
    mock_session.query.assert_called_with(Department)
    mock_session.query().options.assert_called()
    mock_session.query().options().all.assert_called()

def test_department_repository_get_by_id_with_relations(department_repository: DepartmentRepository, mock_session):
    department = Department(id=1, name="Cardiology")
    mock_session.query().options().filter_by().first.return_value = department

    result = department_repository.get_by_id_with_relations(1)

    assert result == department
    mock_session.query.assert_called_with(Department)
    mock_session.query().options.assert_called()
    mock_session.query().options().filter_by.assert_called_with(id=1)
    mock_session.query().options().filter_by().first.assert_called()

def test_ward_repository_get_by_number(ward_repository: WardRepository, mock_session):
    ward = Ward(id=1, number=101, bed_capacity=10)
    mock_session.query().filter_by().first.return_value = ward

    result = ward_repository.get_by_number(101)

    assert result == ward
    mock_session.query.assert_called_with(Ward)
    mock_session.query().filter_by.assert_called_with(number=101)
    mock_session.query().filter_by().first.assert_called()

def test_ward_repository_get_all_with_relations(ward_repository: WardRepository, mock_session):
    wards = [
        Ward(id=1, number=101, bed_capacity=10),
        Ward(id=2, number=102, bed_capacity=20),
    ]
    mock_session.query().options().all.return_value = wards

    result = ward_repository.get_all_with_relations()

    assert result == wards
    mock_session.query.assert_called_with(Ward)
    mock_session.query().options.assert_called()
    mock_session.query().options().all.assert_called()

def test_doctor_repository_get_by_specialization(doctor_repository: DoctorRepository, mock_session):
    doctors = [
        Doctor(id=1, name="Dr. Smith", specialization="Cardiologist"),
        Doctor(id=2, name="Dr. Doe", specialization="Cardiologist"),
    ]
    mock_session.query().filter_by().all.return_value = doctors

    result = doctor_repository.get_by_specialization("Cardiologist")

    assert result == doctors
    mock_session.query.assert_called_with(Doctor)
    mock_session.query().filter_by.assert_called_with(specialization="Cardiologist")
    mock_session.query().filter_by().all.assert_called()

def test_doctor_repository_get_by_department(doctor_repository: DoctorRepository, mock_session):
    doctors = [
        Doctor(id=1, name="Dr. Smith", department_id=1),
        Doctor(id=2, name="Dr. Doe", department_id=1),
    ]
    mock_session.query().filter_by().all.return_value = doctors

    result = doctor_repository.get_by_department(1)

    assert result == doctors
    mock_session.query.assert_called_with(Doctor)
    mock_session.query().filter_by.assert_called_with(department_id=1)
    mock_session.query().filter_by().all.assert_called()

def test_patient_repository_get_by_ward(patient_repository: PatientRepository, mock_session):
    patients = [
        Patient(id=1, name="John Doe", ward_id=1),
        Patient(id=2, name="Jane Doe", ward_id=1),
    ]
    mock_session.query().filter_by().all.return_value = patients

    result = patient_repository.get_by_ward(1)

    assert result == patients
    mock_session.query.assert_called_with(Patient)
    mock_session.query().filter_by.assert_called_with(ward_id=1)
    mock_session.query().filter_by().all.assert_called()

def test_patient_repository_get_by_doctor(patient_repository: PatientRepository, mock_session):
    patients = [
        Patient(id=1, name="John Doe", doctor_id=1),
        Patient(id=2, name="Jane Doe", doctor_id=1),
    ]
    mock_session.query().filter_by().all.return_value = patients

    result = patient_repository.get_by_doctor(1)

    assert result == patients
    mock_session.query.assert_called_with(Patient)
    mock_session.query().filter_by.assert_called_with(doctor_id=1)
    mock_session.query().filter_by().all.assert_called()
