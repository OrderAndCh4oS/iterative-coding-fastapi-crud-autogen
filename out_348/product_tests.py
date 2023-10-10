# filename: product_tests.py
import unittest
from fastapi.testclient import TestClient
from main import app
from database import database, Product
from product_models import CreateProductRequest, UpdateProductRequest
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

class TestProductHandlers(unittest.TestCase):
    def setUp(self):
        database.clear()
        self.uuid = str(uuid4())
        self.product = Product(
            uuid=self.uuid,
            name="Test Product",
            description="This is a test product",
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        database[self.uuid] = self.product

    def test_get_product(self):
        response = client.get(f"/products/{self.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uuid": self.product.uuid,
            "name": self.product.name,
            "description": self.product.description,
            "createdAt": self.product.createdAt.isoformat(),
            "updatedAt": self.product.updatedAt.isoformat(),
        })

    def test_get_all_products(self):
        response = client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.product.model_dump()])

    def test_create_product(self):
        request = CreateProductRequest(
            name="New Product",
            description="This is a new product",
        )
        response = client.post("/products", json=request.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], request.name)
        self.assertEqual(response.json()["description"], request.description)

    def test_update_product(self):
        request = UpdateProductRequest(
            name="Updated Product",
            description="This is an updated product",
        )
        response = client.put(f"/products/{self.uuid}", json=request.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], request.name)
        self.assertEqual(response.json()["description"], request.description)

    def test_delete_product(self):
        response = client.delete(f"/products/{self.uuid}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()