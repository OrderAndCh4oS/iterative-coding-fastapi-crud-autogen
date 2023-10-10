# filename: product_handlers.py

from fastapi import FastAPI, HTTPException
from database import (
    get_product,
    get_all_products,
    create_product as db_create_product,
    update_product,
    delete_product as db_delete_product,
)
from product_models import (
    Product,
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
)
from uuid import uuid4
from datetime import datetime
from typing import List

app = FastAPI()


@app.get("/products/{uuid}", response_model=ProductResponse)
def get_product_detail(uuid: str):
    product = get_product(uuid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products", response_model=List[ProductResponse])
def get_product_list():
    return get_all_products()


@app.post("/products", response_model=ProductResponse)
def create_new_product(request: CreateProductRequest):
    uuid = str(uuid4())
    now = datetime.now()
    product = Product(
        uuid=uuid,
        name=request.name,
        description=request.description,
        createdAt=now,
        updatedAt=now,
    )
    db_create_product(uuid, product)
    return product


@app.put("/products/{uuid}", response_model=ProductResponse)
def update_existing_product(uuid: str, request: UpdateProductRequest):
    product = get_product(uuid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = product.copy(update=request.dict(exclude_unset=True))
    product.updatedAt = datetime.now()
    update_product(uuid, updated_product)
    return updated_product


@app.delete("/products/{uuid}")
def delete_existing_product(uuid: str):
    product = get_product(uuid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_delete_product(uuid)
    return {"detail": "Product deleted"}
