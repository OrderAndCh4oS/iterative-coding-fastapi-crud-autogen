# filename: database.py
from typing import Dict, Optional
from uuid import uuid4
from datetime import datetime
from product_models import Product, CreateProductRequest, UpdateProductRequest

database: Dict[str, Product] = {}

def get_product(uuid: str) -> Optional[Product]:
    return database.get(uuid)

def get_all_products() -> Dict[str, Product]:
    return database

def create_product(request: CreateProductRequest) -> Product:
    uuid = str(uuid4())
    product = Product(
        uuid=uuid,
        name=request.name,
        description=request.description,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )
    database[uuid] = product
    return product

def update_product(uuid: str, request: UpdateProductRequest) -> Product:
    product = database[uuid]
    product.name = request.name
    product.description = request.description
    product.updatedAt = datetime.now()
    database[uuid] = product
    return product

def delete_product(uuid: str) -> None:
    del database[uuid]