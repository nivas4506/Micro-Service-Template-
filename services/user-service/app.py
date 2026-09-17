from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="User Service")

users = []


class User(BaseModel):
    id: int
    name: str
    email: str


@app.get("/health")
def health():
    return {"service": "user-service", "status": "healthy"}


@app.get("/users", response_model=list[User])
def get_users():
    return users


@app.post("/users", response_model=User)
def create_user(user: User):
    users.append(user)
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    return {"id": user_id, "name": "Not Found", "email": ""}
