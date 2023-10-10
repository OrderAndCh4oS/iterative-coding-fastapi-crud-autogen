# filename: product_models.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductEntity(BaseModel):
    uuid: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime

    def model_dump(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }

class CreateProductRequest(BaseModel):
    name: str
    description: str

class UpdateProductRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ProductResponse(BaseModel):
    uuid: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime