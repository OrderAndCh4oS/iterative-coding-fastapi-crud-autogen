# filename: tests.py

import unittest
from fastapi.testclient import TestClient
from main import app
from models import CreateCustomerRequest, UpdateCustomerRequest

client = TestClient(app)

class Tests(unittest.TestCase):
    def test_create_customer(self):
        response = client.post("/customer", json=CreateCustomerRequest(email="test@test.com", username="test").model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"uuid": response.json()["uuid"], "email": "test@test.com", "username": "test", "createdAt": response.json()["createdAt"], "updatedAt": response.json()["updatedAt"]})

    def test_get_customer(self):
        response = client.post("/customer", json=CreateCustomerRequest(email="test@test.com", username="test").model_dump())
        uuid = response.json()["uuid"]
        response = client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"uuid": uuid, "email": "test@test.com", "username": "test", "createdAt": response.json()["createdAt"], "updatedAt": response.json()["updatedAt"]})

    def test_update_customer(self):
        response = client.post("/customer", json=CreateCustomerRequest(email="test@test.com", username="test").model_dump())
        uuid = response.json()["uuid"]
        response = client.put(f"/customer/{uuid}", json=UpdateCustomerRequest(email="updated@test.com", username="updated").model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"uuid": uuid, "email": "updated@test.com", "username": "updated", "createdAt": response.json()["createdAt"], "updatedAt": response.json()["updatedAt"]})

    def test_delete_customer(self):
        response = client.post("/customer", json=CreateCustomerRequest(email="test@test.com", username="test").model_dump())
        uuid = response.json()["uuid"]
        response = client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"detail": "Customer deleted"})

if __name__ == "__main__":
    unittest.main()