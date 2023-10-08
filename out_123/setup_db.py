# filename: setup_db.py

import sqlite3

conn = sqlite3.connect("customers.db")
c = conn.cursor()

c.execute(
    """
    CREATE TABLE customers (
        uuid text primary key,
        email text not null,
        username text not null,
        createdAt text not null,
        updatedAt text not null
    )
"""
)

conn.commit()
conn.close()
