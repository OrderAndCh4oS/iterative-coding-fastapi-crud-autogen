# filename: test_main.py
import unittest
from fastapi.testclient import TestClient
from main import app, Customer, database


class TestFastAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        response = self.client.post(
            "/customer", json={"email": "test@test.com", "username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@test.com")
        self.assertEqual(response.json()["username"], "test")

    def test_read_customers(self):
        response = self.client.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_read_customer(self):
        response = self.client.get("/customer/1")
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        response = self.client.put(
            "/customer/1", json={"email": "test2@test.com", "username": "test2"}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        response = self.client.delete("/customer/1")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
