# filename: models.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class Customer(BaseModel):
    uuid: uuid.UUID
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: datetime


class CreateCustomerRequest(BaseModel):
    email: EmailStr
    username: str


class UpdateCustomerRequest(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
