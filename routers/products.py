from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlmodel import create_engine, SQLModel, Session, select
from datetime import datetime
import contextlib
from schema import Product, ProductsUpdate, ProductsInsert
from db import engine, get_session

router = APIRouter(prefix="/api/products", tags=["products"])

# add product
@router.post("/", response_model=ProductsInsert)
def add_product(product_input: ProductsUpdate, session: Session = Depends(get_session)) -> ProductsInsert:
    db_product = Product.model_validate(product_input)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# get all products
@router.get("/", response_model=list[Product])
def get_products(session: Session = Depends(get_session)) -> list[Product]:
    products = session.exec(select(Product)).all()
    return products

# get product by id
@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)) -> Product:
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# update product by id
@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_input: ProductsUpdate, session: Session = Depends(get_session)) -> Product:
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = Product.model_validate(product_input, product)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# update product price by ProductName
@router.put("/price/{product_name}", response_model=Product)
def update_product_price(product_name: str, product_input: ProductsUpdate, session: Session = Depends(get_session)) -> Product:
    product = session.exec(select(Product).where(Product.ProductName == product_name)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = Product.model_validate(product_input, product)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


#get first 10 products
# @router.get("/first10", response_model=list[Product])
# def get_first10_products(session: Session = Depends(get_session)) -> list[Product]:
#     products = session.exec(select(Product).limit(10)).all()
#     return products
