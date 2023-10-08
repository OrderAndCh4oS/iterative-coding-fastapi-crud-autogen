# filename: main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

# In-memory database
db = {}

# Pydantic models
class Customer(BaseModel):
    uuid: Optional[UUID] = Field(default_factory=uuid4)
    email: str
    username: str
    createdAt: Optional[datetime] = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.now)

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

# Routes
@app.post("/customer", response_model=CustomerResponse)
def create_customer(request: CreateCustomerRequest):
    customer = Customer(**request.dict())
    db[customer.uuid] = customer
    return customer

@app.get("/customer/{uuid}", response_model=CustomerResponse)
def get_customer(uuid: UUID):
    customer = db.get(uuid)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customer/{uuid}", response_model=CustomerResponse)
def update_customer(uuid: UUID, request: UpdateCustomerRequest):
    customer = db.get(uuid)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.email = request.email or customer.email
    customer.username = request.username or customer.username
    customer.updatedAt = datetime.now()
    return customer

@app.delete("/customer/{uuid}")
def delete_customer(uuid: UUID):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    del db[uuid]
    return {"detail": "Customer deleted"}