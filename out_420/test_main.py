# filename: test_main.py

import unittest
from fastapi.testclient import TestClient
from main import app, Customer, CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse
from uuid import UUID
from datetime import datetime

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        request = CreateCustomerRequest(email="test@example.com", username="testuser")
        response = self.client.post("/customer", json=request.dict())
        self.assertEqual(response.status_code, 200)
        response_body = CustomerResponse(**response.json())
        self.assertDictEqual(response_body.dict(), {
            "uuid": response_body.uuid,
            "email": "test@example.com",
            "username": "testuser",
            "createdAt": response_body.createdAt.isoformat(),
            "updatedAt": response_body.updatedAt.isoformat(),
        })

    def test_get_customer(self):
        # Create a customer first
        request = CreateCustomerRequest(email="test@example.com", username="testuser")
        response = self.client.post("/customer", json=request.dict())
        uuid = response.json()["uuid"]

        # Get the customer
        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        response_body = CustomerResponse(**response.json())
        self.assertDictEqual(response_body.dict(), {
            "uuid": response_body.uuid,
            "email": "test@example.com",
            "username": "testuser",
            "createdAt": response_body.createdAt.isoformat(),
            "updatedAt": response_body.updatedAt.isoformat(),
        })

    def test_update_customer(self):
        # Create a customer first
        request = CreateCustomerRequest(email="test@example.com", username="testuser")
        response = self.client.post("/customer", json=request.dict())
        uuid = response.json()["uuid"]

        # Update the customer
        request = UpdateCustomerRequest(email="new@example.com", username="newuser")
        response = self.client.put(f"/customer/{uuid}", json=request.dict())
        self.assertEqual(response.status_code, 200)
        response_body = CustomerResponse(**response.json())
        self.assertDictEqual(response_body.dict(), {
            "uuid": response_body.uuid,
            "email": "new@example.com",
            "username": "newuser",
            "createdAt": response_body.createdAt.isoformat(),
            "updatedAt": response_body.updatedAt.isoformat(),
        })

    def test_delete_customer(self):
        # Create a customer first
        request = CreateCustomerRequest(email="test@example.com", username="testuser")
        response = self.client.post("/customer", json=request.dict())
        uuid = response.json()["uuid"]

        # Delete the customer
        response = self.client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"detail": "Customer deleted"})

if __name__ == "__main__":
    unittest.main()