from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Service")


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int


orders = []


@app.get("/health")
def health():
    return {"service": "order-service", "status": "healthy"}


@app.get("/orders")
def get_orders():
    return orders


@app.post("/orders")
def create_order(order: Order):
    orders.append(order)
    return {
        "message": "Order created",
        "order": order
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order.id == order_id:
            return order

    return {"error": "Order not found"}
