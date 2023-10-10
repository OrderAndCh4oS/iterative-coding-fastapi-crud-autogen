import unittest
from fastapi.testclient import TestClient
from product_handlers import app
from database import database, create_product
from product_models import Product, CreateProductRequest, UpdateProductRequest
from datetime import datetime


class TestProductHandlers(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.uuid = "test_uuid"
        self.product = Product(
            uuid=self.uuid,
            name="Test Product",
            description="This is a test product",
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        create_product(self.uuid, self.product)

    def test_get_product_detail(self):
        response = self.client.get(f"/products/{self.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.product.name)
        self.assertEqual(response.json()["description"], self.product.description)

    def test_get_product_list(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(database))

    def test_create_product(self):
        request = CreateProductRequest(
            name="New Product", description="This is a new product"
        )
        response = self.client.post("/products", json=request.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], request.name)
        self.assertEqual(response.json()["description"], request.description)

    def test_update_product(self):
        request = UpdateProductRequest(
            name="Updated Product", description="Updated description"
        )
        response = self.client.put(f"/products/{self.uuid}", json=request.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], request.name)

    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Product deleted")


if __name__ == "__main__":
    unittest.main()
