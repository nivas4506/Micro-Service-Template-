import importlib.util
from pathlib import Path


def load_app(service: str):
    path = Path(__file__).parent.parent / "services" / service / "app.py"
    spec = importlib.util.spec_from_file_location(f"{service}_app", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app
