from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Product Service")


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


products = []


@app.get("/health")
def health():
    return {"service": "product-service", "status": "healthy"}


@app.get("/products")
def get_products():
    return products


@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product

    return {"error": "Product not found"}
