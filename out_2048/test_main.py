# filename: test_main.py

import unittest
from fastapi.testclient import TestClient
from main import app, CreateCustomerRequest, UpdateCustomerRequest


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test@example.com", username="testuser"
            ).dict(),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(
            data,
            {
                "uuid": data["uuid"],
                "email": "test@example.com",
                "username": "testuser",
                "createdAt": data["createdAt"],
                "updatedAt": data["updatedAt"],
            },
        )

    def test_get_customer(self):
        # Create a customer first
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test2@example.com", username="testuser2"
            ).dict(),
        )
        uuid = response.json()["uuid"]

        # Get the customer
        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(
            data,
            {
                "uuid": uuid,
                "email": "test2@example.com",
                "username": "testuser2",
                "createdAt": data["createdAt"],
                "updatedAt": data["updatedAt"],
            },
        )

    def test_update_customer(self):
        # Create a customer first
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test3@example.com", username="testuser3"
            ).dict(),
        )
        uuid = response.json()["uuid"]

        # Update the customer
        response = self.client.put(
            f"/customer/{uuid}",
            json=UpdateCustomerRequest(email="updated@example.com").dict(),
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertDictEqual(
            data,
            {
                "uuid": uuid,
                "email": "updated@example.com",
                "username": "testuser3",
                "createdAt": data["createdAt"],
                "updatedAt": data["updatedAt"],
            },
        )

    def test_delete_customer(self):
        # Create a customer first
        response = self.client.post(
            "/customer",
            json=CreateCustomerRequest(
                email="test4@example.com", username="testuser4"
            ).dict(),
        )
        uuid = response.json()["uuid"]

        # Delete the customer
        response = self.client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"detail": "Customer deleted"})

        # Try to get the deleted customer
        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
