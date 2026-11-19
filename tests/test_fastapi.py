
import pytest
from fastapi.testclient import TestClient

from fastapi_service.app import main


@pytest.fixture
def client(monkeypatch):
    # Очищаем временное хранилище перед тестом
    main.requests_db.clear()

    # Отключаем реальную отправку сообщений в RabbitMQ
    # Во время тестов RabbitMQ нам не понадобится
    monkeypatch.setattr(
        main,
        "send_maintenance_event",
        lambda event_data: None
    )

    with TestClient(main.app) as test_client:
        yield test_client

    # Очищаем хранилище после теста
    main.requests_db.clear()


def test_health_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_service_name(client):
    response = client.get("/health")

    assert response.json()["service"] == "FastAPI"


def test_get_empty_requests(client):
    response = client.get("/requests")

    assert response.status_code == 200
    assert response.json() == []


def test_create_request(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 1,
            "description": "Проверка оборудования",
            "priority": "high"
        }
    )

    assert response.status_code == 200


def test_create_request_returns_correct_data(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 2,
            "description": "Замена детали",
            "priority": "critical"
        }
    )

    data = response.json()

    assert data["equipment_id"] == 2
    assert data["description"] == "Замена детали"
    assert data["priority"] == "critical"
    assert data["status"] == "new"


def test_default_priority(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 3,
            "description": "Плановый осмотр"
        }
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "medium"


def test_get_requests_after_creation(client):
    client.post(
        "/requests",
        json={
            "equipment_id": 1,
            "description": "Первая заявка",
            "priority": "low"
        }
    )

    response = client.get("/requests")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Первая заявка"


def test_get_request_by_id(client):
    client.post(
        "/requests",
        json={
            "equipment_id": 5,
            "description": "Проверка двигателя",
            "priority": "high"
        }
    )

    response = client.get("/requests/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_missing_request(client):
    response = client.get("/requests/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Заявка не найдена"


def test_empty_description(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 1,
            "description": "",
            "priority": "medium"
        }
    )

    assert response.status_code == 422


def test_blank_description(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 1,
            "description": "   ",
            "priority": "medium"
        }
    )

    assert response.status_code == 422


def test_invalid_priority(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 1,
            "description": "Проверка",
            "priority": "urgent"
        }
    )

    assert response.status_code == 422


def test_zero_equipment_id(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": 0,
            "description": "Проверка",
            "priority": "medium"
        }
    )

    assert response.status_code == 422


def test_negative_equipment_id(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": -1,
            "description": "Проверка",
            "priority": "medium"
        }
    )

    assert response.status_code == 422


def test_invalid_equipment_id_type(client):
    response = client.post(
        "/requests",
        json={
            "equipment_id": "не число",
            "description": "Проверка",
            "priority": "medium"
        }
    )

    assert response.status_code == 422
