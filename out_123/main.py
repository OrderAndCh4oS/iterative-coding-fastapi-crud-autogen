# filename: main.py

from fastapi import FastAPI, HTTPException
from models import CreateCustomerRequest, UpdateCustomerRequest, Customer
from typing import List
import sqlite3
import uuid
from datetime import datetime

app = FastAPI()


def get_db_connection():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/customer", response_model=Customer)
def create_customer(customer: CreateCustomerRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    new_uuid = str(uuid.uuid4())
    created_at = updated_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO customers (uuid, email, username, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?)
    """,
        (new_uuid, customer.email, customer.username, created_at, updated_at),
    )

    conn.commit()
    conn.close()

    return Customer(
        uuid=new_uuid,
        email=customer.email,
        username=customer.username,
        createdAt=created_at,
        updatedAt=updated_at,
    )


@app.get("/customer", response_model=List[Customer])
def read_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM customers").fetchall()

    conn.close()

    return [Customer(**row) for row in rows]


@app.get("/customer/{uuid}", response_model=Customer)
def read_customer(uuid: uuid.UUID):
    conn = get_db_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM customers WHERE uuid = ?", (str(uuid),)
    ).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return Customer(**row)


@app.put("/customer/{uuid}", response_model=Customer)
def update_customer(uuid: uuid.UUID, customer: UpdateCustomerRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    updated_at = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE customers
        SET email = COALESCE(?, email), username = COALESCE(?, username), updatedAt = ?
        WHERE uuid = ?
    """,
        (customer.email, customer.username, updated_at, str(uuid)),
    )

    conn.commit()

    row = cursor.execute(
        "SELECT * FROM customers WHERE uuid = ?", (str(uuid),)
    ).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return Customer(**row)


@app.delete("/customer/{uuid}", response_model=Customer)
def delete_customer(uuid: uuid.UUID):
    conn = get_db_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM customers WHERE uuid = ?", (str(uuid),)
    ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.execute("DELETE FROM customers WHERE uuid = ?", (str(uuid),))

    conn.commit()
    conn.close()

    return Customer(**row)
