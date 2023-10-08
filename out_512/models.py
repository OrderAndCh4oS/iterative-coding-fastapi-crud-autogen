# filename: models.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class Customer(BaseModel):
    uuid: UUID
    email: str
    username: str
    createdAt: datetime
    updatedAt: datetime


class CreateCustomerRequest(BaseModel):
    email: str
    username: str


class UpdateCustomerRequest(BaseModel):
    email: Optional[str]
    username: Optional[str]


class CustomerResponse(BaseModel):
    uuid: UUID
    email: str
    username: str
    createdAt: datetime
    updatedAt: datetime