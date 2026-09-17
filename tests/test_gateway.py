import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


def load_gateway():
    path = Path(__file__).parent.parent / "gateway" / "app.py"
    spec = importlib.util.spec_from_file_location("gateway_app", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


def test_gateway_health():
    client = TestClient(load_gateway())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "api-gateway"
