# filename: main.py

from fastapi import FastAPI, HTTPException
from models import Customer, CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse
from typing import Dict
from datetime import datetime

app = FastAPI()

# In-memory database
db: Dict[str, Customer] = {}

@app.post("/customer", response_model=CustomerResponse)
def create_customer(customer: CreateCustomerRequest):
    new_customer = Customer(**customer.dict())
    db[new_customer.uuid] = new_customer
    return new_customer

@app.get("/customer/{uuid}", response_model=CustomerResponse)
def get_customer(uuid: str):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db[uuid]

@app.put("/customer/{uuid}", response_model=CustomerResponse)
def update_customer(uuid: str, customer: UpdateCustomerRequest):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    updated_customer = db[uuid]
    update_data = customer.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(updated_customer, key, value)
    updated_customer.updatedAt = datetime.now()
    db[uuid] = updated_customer
    return updated_customer

@app.delete("/customer/{uuid}")
def delete_customer(uuid: str):
    if uuid not in db:
        raise HTTPException(status_code=404, detail="Customer not found")
    del db[uuid]
    return {"detail": "Customer deleted"}