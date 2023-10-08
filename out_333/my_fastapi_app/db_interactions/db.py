# filename: my_fastapi_app/db_interactions/db.py

from typing import Dict, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..models.models import Customer

db: Dict[UUID, Customer] = {}

def get_customer(uuid: UUID) -> Optional[Customer]:
    return db.get(uuid)

def create_customer(customer: Customer) -> Customer:
    customer.uuid = uuid4()
    customer.createdAt = datetime.now()
    customer.updatedAt = datetime.now()
    db[customer.uuid] = customer
    return customer

def update_customer(uuid: UUID, customer: Customer) -> Customer:
    existing_customer = get_customer(uuid)
    if existing_customer is None:
        return None
    updated_customer = existing_customer.copy(update=customer.dict(exclude_unset=True))
    updated_customer.updatedAt = datetime.now()
    db[uuid] = updated_customer
    return updated_customer

def delete_customer(uuid: UUID) -> Optional[Customer]:
    return db.pop(uuid, None)