.PHONY: up down build logs test lint clean

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

test:
	python -m pytest tests/ -v

lint:
	python -m pip install ruff --quiet
	ruff check services/ gateway/ tests/

clean:
	docker compose down -v --rmi local

health:
	curl -s http://localhost:8000/health
	curl -s http://localhost:8000/services
