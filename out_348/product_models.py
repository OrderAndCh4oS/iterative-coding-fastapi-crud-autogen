# filename: product_models.py
from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    uuid: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime

class CreateProductRequest(BaseModel):
    name: str
    description: str

class UpdateProductRequest(BaseModel):
    name: str
    description: str