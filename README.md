# Budgix — Budget Tracker

A full-stack budget tracking platform built with **FastAPI** (Python) and **Vue.js 3**, ready for production across three environments: Integration, Staging, and Production.

---

## Features

- **Transactions** — Create, filter, search and paginate income/expense entries
- **Categories & Tags** — Organize spending with custom icons, colors and tags
- **Budgets & Alerts** — Set monthly budgets per category with configurable alert thresholds
- **Dashboard** — Interactive charts: donut (expenses by category), bar (yearly trend), radial (budget usage)
- **CSV/Excel Import** — Bulk import transactions from a file with per-row error reporting
- **Admin Panel** — Platform-wide stats, user management, enable/disable accounts
- **JWT Auth** — Access + refresh token flow, role-based access (user / admin)

---

## Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| Backend     | Python 3.12, FastAPI, SQLAlchemy 2, Alembic     |
| Database    | PostgreSQL 16                                   |
| Frontend    | Vue.js 3, Vite, Pinia, Vue Router, Tailwind CSS |
| Charts      | ApexCharts (vue3-apexcharts)                    |
| Auth        | JWT (python-jose + passlib bcrypt)              |
| Infra       | Docker, Docker Compose, Nginx                   |
| CI/CD       | GitHub Actions                                  |

---

## Project Structure

```
budgix/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/v1/endpoints/ # auth, users, transactions, categories, budgets, dashboard, import, admin
│   │   ├── core/             # config, security, dependencies
│   │   ├── db/               # SQLAlchemy session & base
│   │   ├── models/           # ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # business logic (budget alerts, CSV import)
│   │   └── tests/            # pytest test suite
│   ├── alembic/              # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                 # Vue.js 3 SPA
│   ├── src/
│   │   ├── api/              # Axios client + endpoint helpers
│   │   ├── assets/           # Tailwind CSS
│   │   ├── components/       # layout (AppLayout, NavItem) + ui (modals, cards)
│   │   ├── router/           # Vue Router with auth guards
│   │   ├── stores/           # Pinia stores (auth)
│   │   └── views/            # Dashboard, Transactions, Budgets, Categories, Import, Admin
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── nginx/                    # Reverse proxy config
├── scripts/                  # Dev helper scripts
├── .github/workflows/        # CI/CD pipelines
├── docker-compose.yml        # Local development
├── docker-compose.int.yml    # Integration environment
├── docker-compose.staging.yml
├── docker-compose.prod.yml
└── .env.example
```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- Git

### Quick Start (local dev)

```bash
git clone https://github.com/your-org/budgix.git
cd budgix

# One-command bootstrap
bash scripts/init-dev.sh
```

This will:
1. Copy `.env.example` → `.env` with a generated secret key
2. Start PostgreSQL
3. Run Alembic migrations
4. Start backend (hot-reload) + frontend (Vite dev server)

| Service   | URL                          |
|-----------|------------------------------|
| Frontend  | http://localhost:5173        |
| Backend   | http://localhost:8000        |
| API Docs  | http://localhost:8000/docs   |

### Manual setup

```bash
# Copy env file and edit values
cp .env.example .env

# Start services
docker compose up -d

# Run migrations
docker compose exec backend alembic upgrade head
```

---

## Environments

| Environment | Branch    | Compose file                   | Deployment         |
|-------------|-----------|--------------------------------|--------------------|
| Integration | `develop` | `docker-compose.int.yml`       | Auto on push       |
| Staging     | `main`    | `docker-compose.staging.yml`   | Auto on push       |
| Production  | manual    | `docker-compose.prod.yml`      | Manual + approval  |

Each environment uses its own `.env.<env>` file (never committed). See `.env.example` for all required variables.

---

## CI/CD

Four GitHub Actions pipelines:

| Workflow             | Trigger                        | Action                                        |
|----------------------|--------------------------------|-----------------------------------------------|
| `ci.yml`             | Every push / PR                | Lint, test, build check                       |
| `deploy-int.yml`     | Push to `develop`              | Build → push GHCR → deploy INT                |
| `deploy-staging.yml` | Push to `main`                 | Build → push GHCR → deploy Staging            |
| `deploy-prod.yml`    | Manual (`workflow_dispatch`)   | Requires "deploy" confirmation + env approval |

### Required GitHub Secrets

```
INT_HOST, INT_USER, INT_SSH_KEY, INT_URL
STAGING_HOST, STAGING_USER, STAGING_SSH_KEY, STAGING_URL
PROD_HOST, PROD_USER, PROD_SSH_KEY, PROD_URL
DOCKER_REGISTRY  (e.g. ghcr.io/your-org)
```

---

## API Reference

Full interactive docs available at `/docs` (Swagger UI) and `/redoc` — disabled in production.

### Key Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh

GET    /api/v1/transactions          ?page, size, type, category_id, date_from, date_to, search
POST   /api/v1/transactions
PATCH  /api/v1/transactions/{id}
DELETE /api/v1/transactions/{id}

GET    /api/v1/categories
POST   /api/v1/categories
PATCH  /api/v1/categories/{id}

GET    /api/v1/budgets               ?month, year
POST   /api/v1/budgets

GET    /api/v1/dashboard/summary            ?month, year
GET    /api/v1/dashboard/expenses-by-category
GET    /api/v1/dashboard/monthly-trend      ?year

POST   /api/v1/import/transactions          (multipart CSV/Excel)
GET    /api/v1/import/template

GET    /api/v1/admin/stats                  (admin only)
GET    /api/v1/admin/users
PATCH  /api/v1/admin/users/{id}
```

---

## Development

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
uvicorn app.main:app --reload

# Run tests
pytest app/tests/ -v --cov=app

# Lint
ruff check app/

# Create a new migration
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend

```bash
cd frontend

npm install
npm run dev      # dev server on :5173
npm run build    # production build
npm run lint     # ESLint
```

---

## CSV Import Format

Download the template from `GET /api/v1/import/template` or use this format:

| Column        | Required | Example          |
|---------------|----------|------------------|
| `date`        | ✅       | `2024-01-15`     |
| `amount`      | ✅       | `49.99`          |
| `type`        | ✅       | `expense`        |
| `description` | ✅       | `Supermarché`    |
| `category`    | —        | `Alimentation`   |
| `tags`        | —        | `courses, food`  |
| `note`        | —        | `Carrefour`      |

---

## License

MIT
