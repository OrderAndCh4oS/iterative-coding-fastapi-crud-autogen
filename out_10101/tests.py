# filename: tests.py
import unittest
from fastapi.testclient import TestClient
from main import app
from models import CreateCustomerRequest, UpdateCustomerRequest

class Tests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@test.com")
        self.assertEqual(response.json()["username"], "test")
        self.assertIsNotNone(response.json()["uuid"])
        self.assertIsNotNone(response.json()["createdAt"])
        self.assertIsNotNone(response.json()["updatedAt"])

    def test_get_customers(self):
        response = self.client.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_customer(self):
        # Create a customer first
        create_response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = create_response.json()["uuid"]

        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], uuid)

    def test_update_customer(self):
        # Create a customer first
        create_response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = create_response.json()["uuid"]

        response = self.client.put(f"/customer/{uuid}", json={"email": "updated@test.com", "username": "updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "updated@test.com")
        self.assertEqual(response.json()["username"], "updated")

    def test_delete_customer(self):
        # Create a customer first
        create_response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = create_response.json()["uuid"]

        response = self.client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Customer deleted")

if __name__ == "__main__":
    unittest.main()