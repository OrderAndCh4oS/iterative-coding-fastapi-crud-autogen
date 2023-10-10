# filename: product_tests.py

import unittest
from fastapi.testclient import TestClient
from main import app
from database import db
from product_models import CreateProductRequest, UpdateProductRequest, ProductEntity

class TestProductHandlers(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.product = CreateProductRequest(name="Test Product", description="Test Description").model_dump()
        self.updated_product = UpdateProductRequest(name="Updated Product", description="Updated Description").model_dump()

    def test_create_product(self):
        response = self.client.post("/products/", json=self.product)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), ProductEntity(**db.get(response.json()['uuid'])).model_dump())

    def test_get_product(self):
        response = self.client.post("/products/", json=self.product)
        response = self.client.get(f"/products/{response.json()['uuid']}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), ProductEntity(**db.get(response.json()['uuid'])).model_dump())

    def test_get_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [ProductEntity(**product).model_dump() for product in db.get_all().values()])

    def test_update_product(self):
        response = self.client.post("/products/", json=self.product)
        response = self.client.put(f"/products/{response.json()['uuid']}", json=self.updated_product)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), ProductEntity(**db.get(response.json()['uuid'])).model_dump())

    def test_delete_product(self):
        response = self.client.post("/products/", json=self.product)
        response = self.client.delete(f"/products/{response.json()['uuid']}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()