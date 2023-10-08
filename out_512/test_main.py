# filename: test_main.py

from fastapi.testclient import TestClient
from main import app
from models import CreateCustomerRequest, UpdateCustomerRequest
import unittest

client = TestClient(app)

class TestCustomerAPI(unittest.TestCase):
    def test_create_customer(self):
        request = CreateCustomerRequest(email="test@example.com", username="testuser")
        response = client.post("/customer", json=request.dict())
        self.assertDictEqual(response.json(), request.dict())

    def test_get_customers(self):
        response = client.get("/customer")
        self.assertIsInstance(response.json(), list)

    def test_get_customer(self):
        uuid = "testuuid"  # Replace with a real UUID from the database
        response = client.get(f"/customer/{uuid}")
        self.assertDictEqual(response.json(), {"uuid": uuid})

    def test_update_customer(self):
        uuid = "testuuid"  # Replace with a real UUID from the database
        request = UpdateCustomerRequest(email="new@example.com", username="newuser")
        response = client.put(f"/customer/{uuid}", json=request.dict())
        self.assertDictEqual(response.json(), request.dict())

    def test_delete_customer(self):
        uuid = "testuuid"  # Replace with a real UUID from the database
        response = client.delete(f"/customer/{uuid}")
        self.assertIsNone(response.json())

if __name__ == "__main__":
    unittest.main()