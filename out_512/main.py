# filename: main.py

from fastapi import FastAPI
from models import CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse
from typing import List

app = FastAPI()

@app.post("/customer", response_model=CustomerResponse)
def create_customer_endpoint(request: CreateCustomerRequest) -> CustomerResponse:
    customer = create_customer(request.email, request.username)
    return CustomerResponse(**customer.dict())

@app.get("/customer", response_model=List[CustomerResponse])
def get_customers_endpoint() -> List[CustomerResponse]:
    return [CustomerResponse(**customer.dict()) for customer in db.values()]

@app.get("/customer/{uuid}", response_model=CustomerResponse)
def get_customer_endpoint(uuid: str) -> CustomerResponse:
    customer = get_customer(uuid)
    return CustomerResponse(**customer.dict()) if customer else None

@app.put("/customer/{uuid}", response_model=CustomerResponse)
def update_customer_endpoint(uuid: str, request: UpdateCustomerRequest) -> CustomerResponse:
    customer = update_customer(uuid, request.email, request.username)
    return CustomerResponse(**customer.dict()) if customer else None

@app.delete("/customer/{uuid}")
def delete_customer_endpoint(uuid: str) -> None:
    delete_customer(uuid)