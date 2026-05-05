.PHONY: help dev build rebuild up down logs migrate test lint clean

help:
	@echo ""
	@echo "  Budgix — Commandes disponibles"
	@echo ""
	@echo "  make dev       → Lance l'environnement de dev (rebuild si nécessaire)"
	@echo "  make build     → Build les images Docker"
	@echo "  make rebuild   → Force rebuild sans cache (fix erreurs de packages)"
	@echo "  make up        → Démarre les services"
	@echo "  make down      → Arrête les services"
	@echo "  make logs      → Affiche les logs en temps réel"
	@echo "  make migrate   → Applique les migrations Alembic"
	@echo "  make test      → Lance les tests pytest"
	@echo "  make lint      → Lance ruff sur le backend"
	@echo "  make clean     → Supprime containers + volumes"
	@echo ""

dev: rebuild migrate up
	@echo ""
	@echo "  ✅ Budgix est prêt !"
	@echo "  Frontend  → http://localhost:5173"
	@echo "  Backend   → http://localhost:8000"
	@echo "  API Docs  → http://localhost:8000/docs"
	@echo ""

build:
	docker compose build

rebuild:
	docker compose build --no-cache backend
	docker compose build --no-cache frontend

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose up -d db
	@echo "⏳ Attente PostgreSQL..."
	@sleep 5
	docker compose run --rm backend alembic upgrade head

test:
	docker compose run --rm backend pytest app/tests/ -v --cov=app

lint:
	docker compose run --rm backend ruff check app/

clean:
	docker compose down -v --remove-orphans
	docker image prune -f
