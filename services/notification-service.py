from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")


class Notification(BaseModel):
    user_id: int
    message: str


@app.get("/health")
def health():
    return {
        "service": "notification-service",
        "status": "healthy"
    }


@app.post("/notifications")
def send_notification(notification: Notification):
    return {
        "status": "sent",
        "user_id": notification.user_id,
        "message": notification.message
    }