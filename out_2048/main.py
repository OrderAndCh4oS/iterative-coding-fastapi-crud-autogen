# filename: main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI()

# In-memory database
db = {}


# Pydantic models
class Customer(BaseModel):
    uuid: str
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: datetime


class CreateCustomerRequest(BaseModel):
    email: EmailStr
    username: str


class UpdateCustomerRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class CustomerResponse(BaseModel):
    uuid: str
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: datetime


# Routes
@app.post("/customer", response_model=CustomerResponse)
def create_customer(request: CreateCustomerRequest):
    # Generate a time-ordered UUID
    uuid_str = str(uuid.uuid1())
    now = datetime.now()
    customer = Customer(
        uuid=uuid_str,
        email=request.email,
        username=request.username,
        createdAt=now,
        updatedAt=now,
    )
    db[uuid_str] = customer
    return customer


@app.get("/customer/{uuid}", response_model=CustomerResponse)
def get_customer(uuid: str):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db[uuid]


@app.put("/customer/{uuid}", response_model=CustomerResponse)
def update_customer(uuid: str, request: UpdateCustomerRequest):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = db[uuid]
    if request.email is not None:
        customer.email = request.email
    if request.username is not None:
        customer.username = request.username
    customer.updatedAt = datetime.now()
    db[uuid] = customer
    return customer


@app.delete("/customer/{uuid}")
def delete_customer(uuid: str):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    del db[uuid]
    return {"detail": "Customer deleted"}
