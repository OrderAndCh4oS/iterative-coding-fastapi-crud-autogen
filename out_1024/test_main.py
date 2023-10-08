# filename: test_main.py
import unittest
from fastapi.testclient import TestClient
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_customer(self):
        response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("uuid", response.json())
        self.assertIn("createdAt", response.json())
        self.assertIn("updatedAt", response.json())

    def test_get_customer(self):
        response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = response.json()["uuid"]
        response = self.client.get(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"email": "test@test.com", "username": "test", "uuid": uuid, "createdAt": response.json()["createdAt"], "updatedAt": response.json()["updatedAt"]})

    def test_get_customers(self):
        response = self.client.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_update_customer(self):
        response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = response.json()["uuid"]
        response = self.client.put(f"/customer/{uuid}", json={"email": "test2@test.com", "username": "test2"})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"email": "test2@test.com", "username": "test2", "uuid": uuid, "createdAt": response.json()["createdAt"], "updatedAt": response.json()["updatedAt"]})

    def test_delete_customer(self):
        response = self.client.post("/customer", json={"email": "test@test.com", "username": "test"})
        uuid = response.json()["uuid"]
        response = self.client.delete(f"/customer/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"message": "Customer deleted"})

if __name__ == "__main__":
    unittest.main()