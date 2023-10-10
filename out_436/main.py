# filename: main.py

from fastapi import FastAPI
from product_handlers import router as product_router

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["products"])