# from unittest import mock
# import pytest
# from app.models import Doctor
# from app.models.schemas import DoctorResponseSchema
# from app.services.doctor_service import DoctorService
# from app import create_app
#
#
# @pytest.fixture
# def app():
#     app = create_app()
#     yield app
#     app.container.unwire()
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
#
# def test_add_doctor(client, app):
#     mock_doctor = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=2)
#     doctor_service_mock = mock.Mock(spec=DoctorService)
#     doctor_service_mock.add_doctor.return_value = mock_doctor
#
#     with app.container.doctor_service.override(doctor_service_mock):
#         response = client.post(
#             "/api/doctors",
#             json={"name": "Dr. Smith", "specialization": "Cardiologist", "department_id": 2},
#         )
#
#     assert response.status_code == 201
#     assert response.json == {
#         "id": 1,
#         "name": "Dr. Smith",
#         "specialization": "Cardiologist",
#         "department_id": 2,
#     }
#     doctor_service_mock.add_doctor.assert_called_once_with("Dr. Smith", "Cardiologist", 2)
#
#
# def test_update_doctor(client, app):
#     mock_doctor = Doctor(id=1, name="Dr. John", specialization="Neurologist", department_id=1)
#     doctor_service_mock = mock.Mock(spec=DoctorService)
#     doctor_service_mock.update_doctor.return_value = mock_doctor
#
#     with app.container.doctor_service.override(doctor_service_mock):
#         response = client.put(
#             "/api/doctors/1",
#             json={"name": "Dr. John", "specialization": "Neurologist"},
#         )
#
#     assert response.status_code == 200
#     assert response.json == {
#         "id": 1,
#         "name": "Dr. John",
#         "specialization": "Neurologist",
#         "department_id": 1,
#     }
#     doctor_service_mock.update_doctor.assert_called_once_with(1, name="Dr. John", specialization="Neurologist")
#
#
# def test_get_all_doctors(client, app):
#     mock_doctors = [
#         Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=2),
#         Doctor(id=2, name="Dr. John", specialization="Neurologist", department_id=1),
#     ]
#     doctor_service_mock = mock.Mock(spec=DoctorService)
#     doctor_service_mock.get_all_doctors.return_value = mock_doctors
#
#     with app.container.doctor_service.override(doctor_service_mock):
#         response = client.get("/api/doctors")
#
#     assert response.status_code == 200
#     assert response.json == [
#         {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "department_id": 2},
#         {"id": 2, "name": "Dr. John", "specialization": "Neurologist", "department_id": 1},
#     ]
#     doctor_service_mock.get_all_doctors.assert_called_once()
#
#
# def test_get_doctor_by_id(client, app):
#     mock_doctor = Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=2)
#     doctor_service_mock = mock.Mock(spec=DoctorService)
#     doctor_service_mock.get_doctor_by_id.return_value = mock_doctor
#
#     with app.container.doctor_service.override(doctor_service_mock):
#         response = client.get("/api/doctors/1")
#
#     assert response.status_code == 200
#     assert response.json == {
#         "id": 1,
#         "name": "Dr. Smith",
#         "specialization": "Cardiologist",
#         "department_id": 2,
#     }
#     doctor_service_mock.get_doctor_by_id.assert_called_once_with(1)
#
# def test_get_doctors_by_department(client, app):
#     mock_doctors = [
#         Doctor(id=1, name="Dr. Smith", specialization="Cardiologist", department_id=2),
#         Doctor(id=3, name="Dr. Alice", specialization="Cardiologist", department_id=2),
#     ]
#     doctor_service_mock = mock.Mock(spec=DoctorService)
#     doctor_service_mock.get_doctors_by_department.return_value = mock_doctors
#
#     with app.container.doctor_service.override(doctor_service_mock):
#         response = client.get("/api/doctors/department/2")
#
#     assert response.status_code == 200
#     assert response.json == [
#         {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "department_id": 2},
#         {"id": 3, "name": "Dr. Alice", "specialization": "Cardiologist", "department_id": 2},
#     ]
#     doctor_service_mock.get_doctors_by_department.assert_called_once_with(2)
