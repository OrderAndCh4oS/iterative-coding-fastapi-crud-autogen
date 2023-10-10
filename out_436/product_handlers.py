# filename: product_handlers.py

from fastapi import APIRouter, HTTPException
from database import db
from product_models import ProductEntity, CreateProductRequest, UpdateProductRequest, ProductResponse

router = APIRouter()

@router.get("/{uuid}", response_model=ProductResponse)
def get_product(uuid: str):
    product = db.get(uuid)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductEntity(**product).model_dump()

@router.get("/", response_model=list[ProductResponse])
def get_products():
    return [ProductEntity(**product).model_dump() for product in db.get_all().values()]

@router.post("/", response_model=ProductResponse)
def create_product(product: CreateProductRequest):
    return ProductEntity(**db.create(product.model_dump())).model_dump()

@router.put("/{uuid}", response_model=ProductResponse)
def update_product(uuid: str, product: UpdateProductRequest):
    try:
        return ProductEntity(**db.update(uuid, product.model_dump())).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{uuid}")
def delete_product(uuid: str):
    try:
        db.delete(uuid)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))