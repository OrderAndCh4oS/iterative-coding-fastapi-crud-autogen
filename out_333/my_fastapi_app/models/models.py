# filename: my_fastapi_app/models/models.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class Customer(BaseModel):
    uuid: Optional[UUID]
    email: EmailStr
    username: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class CreateCustomerRequest(BaseModel):
    email: EmailStr
    username: str

class UpdateCustomerRequest(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]

class CustomerResponse(BaseModel):
    uuid: UUID
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: datetime