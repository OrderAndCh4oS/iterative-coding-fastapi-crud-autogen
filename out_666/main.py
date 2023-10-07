# filename: main.py

from fastapi import FastAPI
from models import Customer
from database import database
from typing import List
from uuid import UUID

app = FastAPI()

@app.post("/customer", response_model=Customer)
def create_customer(customer: Customer):
    database[customer.uuid] = customer
    return customer

@app.get("/customer", response_model=List[Customer])
def read_customers():
    return list(database.values())

@app.get("/customer/{uuid}", response_model=Customer)
def read_customer(uuid: UUID):
    return database[str(uuid)]

@app.put("/customer/{uuid}", response_model=Customer)
def update_customer(uuid: UUID, customer: Customer):
    database[str(uuid)] = customer
    return customer

@app.delete("/customer/{uuid}")
def delete_customer(uuid: UUID):
    del database[str(uuid)]
    return {"message": "Customer deleted successfully"}