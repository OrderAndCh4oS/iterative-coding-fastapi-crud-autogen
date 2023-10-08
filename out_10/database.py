# filename: database.py

from models import Customer

database = {}


def get_customer(uuid):
    return database.get(uuid)


def add_customer(customer: Customer):
    database[customer.uuid] = customer


def update_customer(uuid, customer: Customer):
    if uuid in database:
        database[uuid] = customer


def delete_customer(uuid):
    if uuid in database:
        del database[uuid]
