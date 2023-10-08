# filename: test_main.py

from fastapi.testclient import TestClient
from main import app
from models import Customer
from uuid import uuid4

client = TestClient(app)


def test_create_customer():
    response = client.post(
        "/customer", json={"email": "test@example.com", "username": "testuser"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_read_customers():
    response = client.get("/customer")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_customer():
    uuid = str(uuid4())
    client.post(
        "/customer",
        json={"uuid": uuid, "email": "test@example.com", "username": "testuser"},
    )
    response = client.get(f"/customer/{uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == uuid
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_update_customer():
    uuid = str(uuid4())
    client.post(
        "/customer",
        json={"uuid": uuid, "email": "test@example.com", "username": "testuser"},
    )
    response = client.put(
        f"/customer/{uuid}", json={"email": "new@example.com", "username": "newuser"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == uuid
    assert data["email"] == "new@example.com"
    assert data["username"] == "newuser"


def test_delete_customer():
    uuid = str(uuid4())
    client.post(
        "/customer",
        json={"uuid": uuid, "email": "test@example.com", "username": "testuser"},
    )
    response = client.delete(f"/customer/{uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Customer deleted successfully"
