# filename: product_handlers.py
from fastapi import APIRouter, HTTPException
from typing import List
from database import get_product, get_all_products, create_product, update_product, delete_product
from product_models import Product, CreateProductRequest, UpdateProductRequest

router = APIRouter()

@router.get("/products/{uuid}", response_model=Product)
def get_product_handler(uuid: str) -> Product:
    product = get_product(uuid)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.model_dump()

@router.get("/products", response_model=List[Product])
def get_all_products_handler() -> List[Product]:
    return [product.model_dump() for product in get_all_products().values()]

@router.post("/products", response_model=Product)
def create_product_handler(request: CreateProductRequest) -> Product:
    return create_product(request).model_dump()

@router.put("/products/{uuid}", response_model=Product)
def update_product_handler(uuid: str, request: UpdateProductRequest) -> Product:
    product = get_product(uuid)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(uuid, request).model_dump()

@router.delete("/products/{uuid}")
def delete_product_handler(uuid: str) -> None:
    product = get_product(uuid)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_product(uuid)