# filename: models.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CustomerBase(BaseModel):
    email: str
    username: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    uuid: UUID
    createdAt: datetime
    updatedAt: datetime