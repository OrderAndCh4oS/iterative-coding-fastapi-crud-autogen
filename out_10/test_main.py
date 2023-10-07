# filename: test_main.py

import unittest
from fastapi.testclient import TestClient
from main import app
from models import Customer
from uuid import uuid4
from datetime import datetime

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        response = self.client.post("/customer", json={
            "uuid": str(uuid4()),
            "email": "test@example.com",
            "username": "testuser",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Customer created successfully"})

    def test_read_customer(self):
        # Add a test customer
        uuid = str(uuid4())
        self.client.post("/customer", json={
            "uuid": uuid,
            "email": "test@example.com",
            "username": "testuser",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        })

        # Test reading the customer
        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], uuid)
        self.assertEqual(response.json()["email"], "test@example.com")
        self.assertEqual(response.json()["username"], "testuser")

    def test_update_customer(self):
        # Add a test customer
        uuid = str(uuid4())
        self.client.post("/customer", json={
            "uuid": uuid,
            "email": "test@example.com",
            "username": "testuser",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        })

        # Test updating the customer
        response = self.client.put(f"/customer/{uuid}", json={
            "uuid": uuid,
            "email": "updated@example.com",
            "username": "updateduser",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Customer updated successfully"})

    def test_delete_customer(self):
        # Add a test customer
        uuid = str(uuid4())
        self.client.post("/customer", json={
            "uuid": uuid,
            "email": "test@example.com",
            "username": "testuser",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        })

        # Test deleting the customer
        response = self.client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Customer deleted successfully"})

if __name__ == "__main__":
    unittest.main()