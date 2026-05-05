#!/usr/bin/env bash
# Bootstrap local development environment
set -e

echo "🚀 Budgix — Initialisation de l'environnement de développement"

# Check deps
command -v docker >/dev/null 2>&1 || { echo "❌ Docker non trouvé"; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "❌ docker compose non trouvé"; exit 1; }

# Create .env if missing
if [ ! -f .env ]; then
  cp .env.example .env
  # Generate a real secret key
  SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
  sed -i "s/change-me-openssl-rand-hex-32/${SECRET}/" .env
  echo "✅ .env créé avec une clé secrète générée"
fi

# Start DB only
docker compose up -d db
echo "⏳ Attente que PostgreSQL soit prêt..."
sleep 5

# Run migrations
docker compose run --rm backend alembic upgrade head
echo "✅ Migrations appliquées"

# Start all services
docker compose up -d
echo ""
echo "✅ Environnement prêt !"
echo "   Frontend : http://localhost:5173"
echo "   Backend  : http://localhost:8000"
echo "   API Docs : http://localhost:8000/docs"
