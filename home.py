from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, select
from datetime import datetime
import contextlib
from schema import Product, ProductsUpdate, ProductsInsert
from db import engine, Session
from routers import products, web

app = FastAPI(title="Product Management", version="0.1", description="API for Adding and Amending Product Data", openapi_tags=[{"name": "products", "description": "Operations with products"}])
app.include_router(web.router)
app.include_router(products.router)

# uvicorn home:app --reload

@contextlib.asynccontextmanager
async def lifespan(app):
    SQLModel.metadata.create_all(engine)
    try:
        yield
    finally:
        SQLModel.metadata.drop_all(engine)