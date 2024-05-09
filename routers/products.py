from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlmodel import create_engine, SQLModel, Session, select
from datetime import datetime
import contextlib
from schema import Product, ProductsUpdate, ProductsInsert, ProductPrice, ProductPriceByName
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
@router.put("/price/{product_id}", response_model=Product)
def update_product_price_by_id(product_id: int, product_input: ProductPrice, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, product_id)
    if product:
        product.ProductPrice = product_input.ProductPrice
        session.commit()
        return product
    else:
        raise HTTPException(status_code=404, detail=f"No product with id={product_id}")

# Update Stock by Id
@router.put("/stock/{product_id}", response_model=Product)
def update_stock_by_id(product_id: int, product_input: ProductsUpdate, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, product_id)
    if product:
        product.StockQty = product_input.StockQty
        session.commit()
        return product
    else:
        raise HTTPException(status_code=404, detail=f"No product with id {product_id}")

# Get Price by Product Id
@router.get("/price/{product_id}", response_model=Product)
def get_product_price_by_id(product_id: int, session: Session = Depends(get_session)) -> Product:
    product = session.exec(select(Product.ProductPrice).where(Product.id == product_id))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Get Stock by Product Id
@router.get("/stock/{product_id}", response_model=Product)
def get_product_stock_by_id(product_id: int, session: Session = Depends(get_session)) -> Product:
    product = session.exec(select(Product.StockQty).where(Product.id == product_id))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/price/{product_name}", response_model=ProductPriceByName)
def get_product_price_by_name(product_name: str, session: Session = Depends(get_session)) -> ProductPriceByName:
    product = session.exec(select(Product.ProductPrice).where(Product.ProductName == product_name))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
