# filename: main.py
from fastapi import FastAPI
from models import Customer, CustomerCreate, CustomerUpdate
from uuid import uuid4
from datetime import datetime

app = FastAPI()

# In-memory database
db = []

@app.post("/customer")
def create_customer(customer: CustomerCreate):
    customer_data = customer.dict(by_alias=True)
    customer_data["uuid"] = uuid4()
    customer_data["createdAt"] = datetime.now()
    customer_data["updatedAt"] = datetime.now()
    db.append(customer_data)
    return customer_data

@app.get("/customer/{uuid}")
def get_customer(uuid: str):
    for customer in db:
        if customer["uuid"] == uuid:
            return customer
    return {"error": "Customer not found"}

@app.get("/customer")
def get_customers():
    return db

@app.put("/customer/{uuid}")
def update_customer(uuid: str, customer: CustomerUpdate):
    for index, existing_customer in enumerate(db):
        if existing_customer["uuid"] == uuid:
            updated_customer = customer.dict(by_alias=True)
            updated_customer["uuid"] = uuid
            updated_customer["createdAt"] = existing_customer["createdAt"]
            updated_customer["updatedAt"] = datetime.now()
            db[index] = updated_customer
            return updated_customer
    return {"error": "Customer not found"}

@app.delete("/customer/{uuid}")
def delete_customer(uuid: str):
    for index, existing_customer in enumerate(db):
        if existing_customer["uuid"] == uuid:
            del db[index]
            return {"message": "Customer deleted"}
    return {"error": "Customer not found"}