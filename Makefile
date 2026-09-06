.PHONY: help dev up down logs backend frontend test pytest clean

help:
	@echo "Job Intelligence Platform - Makefile Commands"
	@echo "------------------------------------------------"
	@echo "make dev       - Run backend and frontend locally"
	@echo "make up        - Start all services with Docker Compose"
	@echo "make down      - Stop and remove Docker Compose containers"
	@echo "make logs      - View logs from Docker Compose services"
	@echo "make backend   - Start backend locally using Uvicorn"
	@echo "make frontend  - Start frontend locally using Vite"
	@echo "make test      - Run backend unit tests with pytest"
	@echo "make clean     - Clean temporary build and python cache files"

dev:
	@echo "Starting development environment..."
	@echo "Run 'make backend' in one terminal and 'make frontend' in another."

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
