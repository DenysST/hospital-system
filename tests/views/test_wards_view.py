from unittest import mock
import pytest
from app.models import Ward
from app.services.ward_service import WardService
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_ward(client, app):
    mock_ward = Ward(id=1, number=101, bed_capacity=20, department_id=2)
    ward_service_mock = mock.Mock(spec=WardService)
    ward_service_mock.add_ward.return_value = mock_ward

    with app.container.ward_service.override(ward_service_mock):
        response = client.post(
            "/api/wards",
            json={"number": 101, "bed_capacity": 20, "department_id": 2},
        )

    assert response.status_code == 201
    assert response.json == {
        "id": 1,
        "number": 101,
        "bed_capacity": 20,
        "department_id": 2,
    }
    ward_service_mock.add_ward.assert_called_once_with(101, 20, 2)

def test_update_ward(client, app):
    mock_ward = Ward(id=1, number=101, bed_capacity=25, department_id=2)
    ward_service_mock = mock.Mock(spec=WardService)
    ward_service_mock.update_ward.return_value = mock_ward

    with app.container.ward_service.override(ward_service_mock):
        response = client.put(
            "/api/wards/1",
            json={"bed_capacity": 25},
        )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "number": 101,
        "bed_capacity": 25,
        "department_id": 2,
    }
    ward_service_mock.update_ward.assert_called_once_with(1, bed_capacity=25)

def test_get_all_wards(client, app):
    mock_wards = [
        Ward(id=1, number=101, bed_capacity=20, department_id=2),
        Ward(id=2, number=102, bed_capacity=15, department_id=3),
    ]
    ward_service_mock = mock.Mock(spec=WardService)
    ward_service_mock.get_all_wards.return_value = mock_wards

    with app.container.ward_service.override(ward_service_mock):
        response = client.get("/api/wards")

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "number": 101, "bed_capacity": 20, "department_id": 2},
        {"id": 2, "number": 102, "bed_capacity": 15, "department_id": 3},
    ]
    ward_service_mock.get_all_wards.assert_called_once()

def test_get_ward_by_id(client, app):
    mock_ward = Ward(id=1, number=101, bed_capacity=20, department_id=2)
    ward_service_mock = mock.Mock(spec=WardService)
    ward_service_mock.get_ward_by_id.return_value = mock_ward

    with app.container.ward_service.override(ward_service_mock):
        response = client.get("/api/wards/1")

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "number": 101,
        "bed_capacity": 20,
        "department_id": 2,
    }
    ward_service_mock.get_ward_by_id.assert_called_once_with(1)
