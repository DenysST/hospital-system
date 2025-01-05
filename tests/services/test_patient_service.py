from datetime import datetime, timedelta

import pytest
from app.models import Patient, Ward, Doctor, Department
from app.services.patient_service import PatientService, GeminiService, NotificationService
from app.consts import DEPARTMENT, UNKNOWN_DEPARTMENT, PLANED_HOSPITALISATION_DAYS, EMAIL_SUBJECT, EMAIL_BODY
from app.repositories import PatientRepository, WardRepository, DoctorRepository, DepartmentRepository


@pytest.fixture
def mock_patient_repository(mocker):
    return mocker.create_autospec(PatientRepository)

@pytest.fixture
def mock_ward_repository(mocker):
    return mocker.create_autospec(WardRepository)

@pytest.fixture
def mock_doctor_repository(mocker):
    return mocker.create_autospec(DoctorRepository)

@pytest.fixture
def mock_department_repository(mocker):
    return mocker.create_autospec(DepartmentRepository)

@pytest.fixture
def mock_gemini_service(mocker):
    return mocker.create_autospec(GeminiService)

@pytest.fixture
def mock_notification_service(mocker):
    return mocker.create_autospec(NotificationService)

@pytest.fixture
def service(mock_patient_repository, mock_ward_repository, mock_doctor_repository,
            mock_department_repository, mock_gemini_service, mock_notification_service):
    return PatientService(
        mock_patient_repository, mock_ward_repository, mock_doctor_repository,
        mock_department_repository, mock_gemini_service, mock_notification_service
    )


def test_add_patient_success(service, mock_patient_repository, mock_gemini_service,
                             mock_department_repository, mock_notification_service):
    mock_gemini_service.get_assigment.return_value = {
        DEPARTMENT: "Cardiology",
        PLANED_HOSPITALISATION_DAYS: 5
    }
    doctor = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", email="smith@example.com", patients=[])
    ward = Ward(id=1, number=101, bed_capacity=10, patients=[])
    department = Department(id=1, name="Cardiology", doctors=[doctor], wards=[ward])
    mock_department_repository.get_by_name.return_value = department
    created_patient = Patient(
        id=1, name="John Doe", problem="Heart Disease", ward_id=1, doctor_id=1,
        hospitalisation_start_date=datetime.now(),
        hospitalisation_end_date=datetime.now() + timedelta(days=5)
    )
    created_patient.doctor = doctor
    mock_patient_repository.add.return_value = created_patient

    patient = service.add_patient("John Doe", "Heart Disease")

    assert patient.id == 1
    assert patient.name == "John Doe"
    assert patient.problem == "Heart Disease"
    mock_gemini_service.get_assigment.assert_called_once_with("Heart Disease")
    mock_department_repository.get_by_name.assert_called_once_with("Cardiology")
    mock_patient_repository.add.assert_called_once()
    mock_notification_service.send_email.assert_called_once_with(
        "smith@example.com",
        EMAIL_SUBJECT,
        EMAIL_BODY.format(created_patient=created_patient, name="John Doe", problem="Heart Disease")
    )

def test_add_patient_invalid_problem(service, mock_gemini_service):
    mock_gemini_service.get_assigment.return_value = {DEPARTMENT: UNKNOWN_DEPARTMENT}

    with pytest.raises(ValueError, match="Invalid patient problem. Cannot assign to a department."):
        service.add_patient("John Doe", "Unknown Problem")

    mock_gemini_service.get_assigment.assert_called_once_with("Unknown Problem")

def test_update_patient_success(service, mock_patient_repository, mock_ward_repository, mock_doctor_repository):
    mock_patient = Patient(id=1, name="John Doe", ward_id=1, doctor_id=1)
    updated_patient = Patient(id=1, name="John Doe", ward_id=2, doctor_id=2)

    mock_patient_repository.get_by_id.return_value = mock_patient
    mock_ward_repository.get_by_id.return_value = Ward(id=2, department_id=1, patients=[], bed_capacity=10)
    mock_doctor_repository.get_by_id.return_value = Doctor(id=2, department_id=1)
    mock_patient_repository.update.return_value = updated_patient

    result = service.update_patient(1, ward_id=2, doctor_id=2)

    assert result.ward_id == 2
    assert result.doctor_id == 2
    assert result.name == "John Doe"
    mock_patient_repository.get_by_id.assert_called_once_with(1)
    assert mock_ward_repository.get_by_id.call_count == 2
    mock_ward_repository.get_by_id.assert_any_call(2)
    mock_doctor_repository.get_by_id.assert_called_once_with(2)
    mock_patient_repository.update.assert_called_once_with(mock_patient)

def test_update_patient_not_found(service, mock_patient_repository):
    mock_patient_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Patient not found."):
        service.update_patient(999, ward_id=1)

    mock_patient_repository.get_by_id.assert_called_once_with(999)

def test_get_patient_by_id_success(service, mock_patient_repository):
    mock_patient_repository.get_by_id.return_value = Patient(id=1, name="John Doe")

    patient = service.get_patient_by_id(1)

    assert patient.id == 1
    assert patient.name == "John Doe"
    mock_patient_repository.get_by_id.assert_called_once_with(1)

def test_get_patient_by_id_not_found(service, mock_patient_repository):
    mock_patient_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Patient not found."):
        service.get_patient_by_id(999)

    mock_patient_repository.get_by_id.assert_called_once_with(999)

def test_get_all_patients(service, mock_patient_repository):
    mock_patient_repository.get_all.return_value = [
        Patient(id=1, name="John Doe"),
        Patient(id=2, name="Jane Doe")
    ]

    patients = service.get_all_patients()

    assert len(patients) == 2
    assert patients[0].name == "John Doe"
    assert patients[1].name == "Jane Doe"
    mock_patient_repository.get_all.assert_called_once()

def test_get_patients_by_ward(service, mock_patient_repository):
    mock_patient_repository.get_by_ward.return_value = [
        Patient(id=1, name="John Doe"),
        Patient(id=2, name="Jane Doe")
    ]

    patients = service.get_patients_by_ward(1)

    assert len(patients) == 2
    assert patients[0].name == "John Doe"
    assert patients[1].name == "Jane Doe"
    mock_patient_repository.get_by_ward.assert_called_once_with(1)

def test_get_patients_by_doctor(service, mock_patient_repository):
    mock_patient_repository.get_by_doctor.return_value = [
        Patient(id=1, name="John Doe"),
        Patient(id=2, name="Jane Doe")
    ]

    patients = service.get_patients_by_doctor(1)

    assert len(patients) == 2
    assert patients[0].name == "John Doe"
    assert patients[1].name == "Jane Doe"
    mock_patient_repository.get_by_doctor.assert_called_once_with(1)
