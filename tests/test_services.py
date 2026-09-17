from fastapi.testclient import TestClient

from conftest import load_app


def test_user_service_health():
    client = TestClient(load_app("user-service"))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "user-service"


def test_product_service_health():
    client = TestClient(load_app("product-service"))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "product-service"


def test_order_service_health():
    client = TestClient(load_app("order-service"))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "order-service"


def test_payment_service_health():
    client = TestClient(load_app("payment-service"))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "payment-service"


def test_notification_service_health():
    client = TestClient(load_app("notification-service"))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "notification-service"
