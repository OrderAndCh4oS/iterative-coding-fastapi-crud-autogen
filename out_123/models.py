# filename: models.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class Customer(BaseModel):
    uuid: str = str(uuid.uuid4())
    email: EmailStr
    username: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

class CreateCustomerRequest(BaseModel):
    email: EmailStr
    username: str

class UpdateCustomerRequest(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]

class CustomerResponse(BaseModel):
    uuid: str
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: datetime