# filename: models.py
from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    uuid: str
    email: str
    username: str
    createdAt: datetime
    updatedAt: datetime

class CreateCustomerRequest(BaseModel):
    email: str
    username: str

class UpdateCustomerRequest(BaseModel):
    email: str = None
    username: str = None

class CustomerResponse(BaseModel):
    uuid: str
    email: str
    username: str
    createdAt: datetime
    updatedAt: datetime