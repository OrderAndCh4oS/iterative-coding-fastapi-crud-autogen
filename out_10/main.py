# filename: main.py

from fastapi import FastAPI
from models import Customer
from database import get_customer, add_customer, update_customer, delete_customer
from uuid import UUID

app = FastAPI()


@app.post("/customer")
async def create_customer_handler(customer: Customer):
    add_customer(customer)
    return {"message": "Customer created successfully"}


@app.get("/customer/{uuid}")
async def read_customer_handler(uuid: UUID):
    customer = get_customer(uuid)
    if customer is None:
        return {"message": "Customer not found"}
    return customer


@app.put("/customer/{uuid}")
async def update_customer_handler(uuid: UUID, customer: Customer):
    update_customer(uuid, customer)
    return {"message": "Customer updated successfully"}


@app.delete("/customer/{uuid}")
async def delete_customer_handler(uuid: UUID):
    delete_customer(uuid)
    return {"message": "Customer deleted successfully"}
