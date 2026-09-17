from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Payment Service")


class Payment(BaseModel):
    order_id: int
    amount: float


@app.get("/health")
def health():
    return {"service": "payment-service", "status": "healthy"}


@app.post("/payments")
def process_payment(payment: Payment):
    return {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "success",
        "transaction_id": f"TXN-{payment.order_id}"
    }
