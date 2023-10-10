# filename: database.py

# This will be our in-memory database
database = {}

def get_product(uuid):
    return database.get(uuid)

def get_all_products():
    return list(database.values())

def create_product(uuid, product):
    database[uuid] = product

def update_product(uuid, product):
    database[uuid] = product

def delete_product(uuid):
    del database[uuid]