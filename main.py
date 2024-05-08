import io
import os
import pandas as pd
import time
import sqlite3
import mysql.connector
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validate_email
from dotenv import load_dotenv, dotenv_values

load_dotenv() #Loads environment variables

MYSQL_HOST       = os.environ['MYSQL_HOST']
MYSQL_USER         = os.environ['MYSQL_USER']
MYSQL_PASSWORD    = os.environ['MYSQL_PASSWORD']
MYSQL_PORT      = os.environ['MYSQL_PORT']


mydb = mysql.connector.connect(
  host      =   MYSQL_HOST,
  user      =   MYSQL_USER,
  password  =   MYSQL_PASSWORD,
  port      =   MYSQL_PORT,
  database  =   'GeneralDB'
)


app = FastAPI()

class Product(BaseModel):
    name: str = Field(..., title="Product Name", description="Name of the product")
    price: float = Field(..., title="Product Price", description="Price of the product")
    stock: int = Field(..., title="Product Stock", description="Stock of the product")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/products/")
def create_product(product: Product):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Products (name, price, stock) VALUES (%s, %s, %s)"
    val = (product.name, product.price, product.stock)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"name": product.name, "price": product.price, "stock": product.stock}

@app.get("/products/")
def read_products():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Products")
    myresult = mycursor.fetchall()
    return myresult

@app.get("/products/{product_id}")
def read_product(product_id: int):
    mycursor = mydb.cursor()
    if not mycursor.execute("SELECT * FROM Products WHERE id = %s", (product_id,)):
        raise HTTPException(status_code=404, detail="Product not found")
    myresult = mycursor.fetchall()
    return myresult
