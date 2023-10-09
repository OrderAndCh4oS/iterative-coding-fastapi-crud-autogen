# filename: main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from models import Customer, CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse
from typing import List
from uuid import uuid4
from datetime import datetime

class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message

app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )

# In-memory database
db = {}

@app.post("/customer", response_model=CustomerResponse)
def create_customer(request: CreateCustomerRequest):
    # Validate request data
    if not request.email or not request.username:
        raise ValidationError("Email and username are required")

    uuid = str(uuid4())
    now = datetime.now()
    customer = Customer(uuid=uuid, email=request.email, username=request.username, createdAt=now, updatedAt=now)
    db[uuid] = customer
    return customer

@app.get("/customer", response_model=List[CustomerResponse])
def get_customers():
    return list(db.values())

@app.get("/customer/{uuid}", response_model=CustomerResponse)
def get_customer(uuid: str):
    if uuid not in db:
        raise NotFoundError("Customer not found")
    return db[uuid]

@app.put("/customer/{uuid}", response_model=CustomerResponse)
def update_customer(uuid: str, request: UpdateCustomerRequest):
    if uuid not in db:
        raise NotFoundError("Customer not found")
    updated_customer = db[uuid].copy(update=request.dict(exclude_unset=True))
    updated_customer.updatedAt = datetime.now()
    db[uuid] = updated_customer
    return updated_customer

@app.delete("/customer/{uuid}")
def delete_customer(uuid: str):
    if uuid not in db:
        raise NotFoundError("Customer not found")
    del db[uuid]
    return {"detail": "Customer deleted"}