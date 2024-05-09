from sqlmodel import SQLModel, Field

# Inherits from SQLModel
class ProductsUpdate(SQLModel):
    ProductName: str = "Product abc"
    ProductPrice: float|None = 9.99
    StockQty: int|None = 0

class ProductPrice(ProductsUpdate):
    ProductPrice: float

# Inherits from ProductsUpdate but adds the id field
class Product(ProductsUpdate, table=True):
    id: int = Field(default=None, primary_key=True)

class ProductsInsert(ProductsUpdate):
    id: int

class ProductPriceByName(ProductsUpdate):
    ProductName: str
    ProductPrice: float
