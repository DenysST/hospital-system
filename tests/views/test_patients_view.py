from unittest import mock
import pytest
from app.models import Patient
from app.services.patient_service import PatientService
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_patient(client, app):
    mock_patient = Patient(id=1, name="John Doe", problem="High fever", ward_id=2, doctor_id=3)
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.add_patient.return_value = mock_patient

    with app.container.patient_service.override(patient_service_mock):
        response = client.post(
            "/patients",
            json={"name": "John Doe", "problem": "High fever"},
        )

    assert response.status_code == 201
    assert response.json == {
        "id": 1,
        "hospitalisation_end_date": None,
        "hospitalisation_start_date": None,
        "name": "John Doe",
        "problem": "High fever",
        "ward_id": 2,
        "doctor_id": 3
    }

    patient_service_mock.add_patient.assert_called_once_with(name="John Doe", problem="High fever")

def test_update_patient(client, app):
    mock_patient = Patient(id=1, name="Jane Doe", problem="Cold", ward_id=2, doctor_id=3)
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.update_patient.return_value = mock_patient

    with app.container.patient_service.override(patient_service_mock):
        response = client.put(
            "/patients/1",
            json={"name": "Jane Doe"},
        )

    assert response.status_code == 200
    assert response.json == {"id": 1, "hospitalisation_end_date": None,
                             "hospitalisation_start_date": None, "name": "Jane Doe", "problem": "Cold", "ward_id": 2,
                             "doctor_id": 3}
    patient_service_mock.update_patient.assert_called_once_with(1, name="Jane Doe")

def test_get_all_patients(client, app):
    mock_patients = [
        Patient(id=1, name="John Doe", problem="High fever", ward_id=2, doctor_id=3),
        Patient(id=2, name="Jane Doe", problem="Cold", ward_id=2, doctor_id=3),
    ]
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.get_all_patients.return_value = mock_patients

    with app.container.patient_service.override(patient_service_mock):
        response = client.get("/patients")

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "John Doe", "problem": "High fever", "ward_id": 2, "doctor_id": 3},
        {"id": 2, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "Jane Doe", "problem": "Cold", "ward_id": 2, "doctor_id": 3},
    ]
    patient_service_mock.get_all_patients.assert_called_once()

def test_get_patients_by_ward(client, app):
    mock_patients = [
        Patient(id=1, name="John Doe", problem="High fever", ward_id=2, doctor_id=3),
        Patient(id=3, name="Alice Brown", problem="Pneumonia", ward_id=2, doctor_id=3),
    ]
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.get_patients_by_ward.return_value = mock_patients

    with app.container.patient_service.override(patient_service_mock):
        response = client.get("/patients/ward/2")

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "John Doe", "problem": "High fever", "ward_id": 2, "doctor_id": 3},
        {"id": 3, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "Alice Brown", "problem": "Pneumonia", "ward_id": 2,
         "doctor_id": 3},
    ]
    patient_service_mock.get_patients_by_ward.assert_called_once_with(2)

def test_get_patients_by_doctor(client, app):
    mock_patients = [
        Patient(id=2, name="Jane Doe", problem="Cold", ward_id=2, doctor_id=3),
        Patient(id=4, name="Bob Green", problem="Fracture", ward_id=2, doctor_id=3),
    ]
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.get_patients_by_doctor.return_value = mock_patients

    with app.container.patient_service.override(patient_service_mock):
        response = client.get("/patients/doctor/3")

    assert response.status_code == 200
    assert response.json == [
        {"id": 2, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "Jane Doe", "problem": "Cold", "ward_id": 2, "doctor_id": 3},
        {"id": 4, "hospitalisation_end_date": None,
         "hospitalisation_start_date": None, "name": "Bob Green", "problem": "Fracture", "ward_id": 2, "doctor_id": 3},
    ]
    patient_service_mock.get_patients_by_doctor.assert_called_once_with(3)

def test_get_patient_by_id(client, app):
    mock_patient = Patient(id=1, name="John Doe", problem="High fever", ward_id=2, doctor_id=3)
    patient_service_mock = mock.Mock(spec=PatientService)
    patient_service_mock.get_patient_by_id.return_value = mock_patient

    with app.container.patient_service.override(patient_service_mock):
        response = client.get("/patients/1")

    assert response.status_code == 200
    assert response.json == {"id": 1, "hospitalisation_end_date": None,
                             "hospitalisation_start_date": None, "name": "John Doe", "problem": "High fever",
                             "ward_id": 2, "doctor_id": 3}
    patient_service_mock.get_patient_by_id.assert_called_once_with(1)
