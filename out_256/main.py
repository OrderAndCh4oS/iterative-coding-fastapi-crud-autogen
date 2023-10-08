# filename: main.py
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import uuid
import datetime

app = FastAPI()


class Customer(BaseModel):
    email: str
    username: str


class CustomerInDB(Customer):
    uuid: str
    createdAt: str
    updatedAt: str


database = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/customer", response_model=CustomerInDB)
def create_customer(customer: Customer):
    customer_id = str(uuid.uuid1())
    now = datetime.datetime.now().isoformat()
    customer_in_db = CustomerInDB(
        uuid=customer_id, createdAt=now, updatedAt=now, **customer.dict()
    )
    database[customer_id] = customer_in_db
    return customer_in_db


@app.get("/customer", response_model=list[CustomerInDB])
def read_customers():
    return list(database.values())


@app.get("/customer/{customer_id}", response_model=CustomerInDB)
def read_customer(customer_id: str):
    if customer_id not in database:
        raise HTTPException(status_code=404, detail="Customer not found")
    return database[customer_id]


@app.put("/customer/{customer_id}", response_model=CustomerInDB)
def update_customer(customer_id: str, customer: Customer):
    if customer_id not in database:
        raise HTTPException(status_code=404, detail="Customer not found")
    database[customer_id].email = customer.email
    database[customer_id].username = customer.username
    database[customer_id].updatedAt = datetime.datetime.now().isoformat()
    return database[customer_id]


@app.delete("/customer/{customer_id}")
def delete_customer(customer_id: str):
    if customer_id not in database:
        raise HTTPException(status_code=404, detail="Customer not found")
    del database[customer_id]
    return {"detail": "Customer deleted"}
