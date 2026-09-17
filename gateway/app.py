import httpx
from fastapi import FastAPI

app = FastAPI(title="MicroDeploy API Gateway")

SERVICES = {
    "users": "http://user-service:8001",
    "products": "http://product-service:8002",
    "orders": "http://order-service:8003",
    "payments": "http://payment-service:8004",
    "notifications": "http://notification-service:8005",
}


@app.get("/health")
def health():
    return {
        "service": "api-gateway",
        "status": "healthy"
    }


@app.get("/services")
async def services():
    result = {}

    async with httpx.AsyncClient() as client:
        for name, url in SERVICES.items():
            try:
                response = await client.get(f"{url}/health")
                result[name] = response.json()
            except Exception:  # noqa: BLE001
                result[name] = {"status": "unavailable"}

    return result


@app.get("/users")
async def users():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICES['users']}/users"
        )

    return response.json()


@app.get("/products")
async def products():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICES['products']}/products"
        )

    return response.json()


@app.get("/orders")
async def orders():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICES['orders']}/orders"
        )

    return response.json()