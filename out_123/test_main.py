# filename: test_main.py

import unittest
import main
import uuid
from fastapi.testclient import TestClient
from models import CreateCustomerRequest, UpdateCustomerRequest, Customer
import json


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_create_customer(self):
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test@example.com", username="testuser"
            ).dict(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), json.loads(Customer(**response.json()).json())
        )

    def test_read_customers(self):
        response = self.client.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_read_customer(self):
        # Create a customer to test with
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test@example.com", username="testuser"
            ).dict(),
        )
        test_uuid = response.json()["uuid"]

        response = self.client.get(f"/customer/{test_uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), json.loads(Customer(**response.json()).json())
        )

    def test_update_customer(self):
        # Create a customer to test with
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test@example.com", username="testuser"
            ).dict(),
        )
        test_uuid = response.json()["uuid"]

        response = self.client.put(
            f"/customer/{test_uuid}",
            json=UpdateCustomerRequest(
                email="new@example.com", username="newuser"
            ).dict(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), json.loads(Customer(**response.json()).json())
        )

    def test_delete_customer(self):
        # Create a customer to test with
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test@example.com", username="testuser"
            ).dict(),
        )
        test_uuid = response.json()["uuid"]

        response = self.client.delete(f"/customer/{test_uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), json.loads(Customer(**response.json()).json())
        )


if __name__ == "__main__":
    unittest.main()
