# from unittest import mock
# import pytest
# from app.models import Department, DepartmentOccupancySchema
# from app.services.department_service import DepartmentService
# from app import create_app
#
#
# @pytest.fixture
# def app():
#     app = create_app()
#     yield app
#     app.container.unwire()
#
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
# def test_update_department(client, app):
#     mock_department = Department(id=1, name="Updated Cardiology")
#     department_service_mock = mock.Mock(spec=DepartmentService)
#     department_service_mock.update_department.return_value = mock_department
#
#     with app.container.department_service.override(department_service_mock):
#         response = client.put(
#             "/api/departments/1",
#             json={"name": "Updated Cardiology"}
#         )
#
#     assert response.status_code == 200
#     assert response.json == {"id": 1, "name": "Updated Cardiology", "wards": [], "doctors": []}
#     department_service_mock.update_department.assert_called_once_with(1, "Updated Cardiology")
#
# def test_get_all_departments(client, app):
#     mock_departments = [
#         Department(id=1, name="Cardiology"),
#         Department(id=2, name="Neurology"),
#     ]
#     department_service_mock = mock.Mock(spec=DepartmentService)
#     department_service_mock.get_all_departments.return_value = mock_departments
#
#     with app.container.department_service.override(department_service_mock):
#         response = client.get("/api/departments")
#
#     assert response.status_code == 200
#     assert response.json == [
#         {"id": 1, "name": "Cardiology", "wards": [], "doctors": []},
#         {"id": 2, "name": "Neurology", "wards": [], "doctors": []},
#     ]
#     department_service_mock.get_all_departments.assert_called_once_with(with_relations=True)
#
# def test_get_department_by_id(client, app):
#     mock_department = Department(id=1, name="Cardiology")
#     department_service_mock = mock.Mock(spec=DepartmentService)
#     department_service_mock.get_department_by_id.return_value = mock_department
#
#     with app.container.department_service.override(department_service_mock):
#         response = client.get("/api/departments/1")
#
#     assert response.status_code == 200
#     assert response.json == {"id": 1, "name": "Cardiology", "wards": [], "doctors": []}
#     department_service_mock.get_department_by_id.assert_called_once_with(1)
#
# def test_get_bed_occupancy(client, app):
#     mock_occupancy_data = [
#         DepartmentOccupancySchema(
#             department_id=1,
#             department_name="Cardiology",
#             total_beds=50,
#             occupied_beds=30,
#             occupancy_percentage=60.0,
#         ),
#         DepartmentOccupancySchema(
#             department_id=2,
#             department_name="Neurology",
#             total_beds=40,
#             occupied_beds=20,
#             occupancy_percentage=50.0,
#         ),
#     ]
#     department_service_mock = mock.Mock(spec=DepartmentService)
#     department_service_mock.calculate_bed_occupancy.return_value = mock_occupancy_data
#
#     with app.container.department_service.override(department_service_mock):
#         response = client.get("/api/departments/occupancy")
#
#     assert response.status_code == 200
#     assert response.json == [data.model_dump() for data in mock_occupancy_data]
#     department_service_mock.calculate_bed_occupancy.assert_called_once()
