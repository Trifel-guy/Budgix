# Budgix — Backend

FastAPI REST API for the Budgix budget tracking platform.

## Stack

- **Python 3.12** + **FastAPI 0.111**
- **PostgreSQL 16** via SQLAlchemy 2 (sync)
- **Alembic** for schema migrations
- **Pydantic v2** for request/response validation
- **python-jose** + **passlib** for JWT auth (bcrypt)
- **pandas** + **openpyxl** for CSV/Excel import
- **pytest** + **pytest-cov** for testing

## Structure

```
app/
├── api/v1/
│   ├── router.py              # Aggregates all routers
│   └── endpoints/
│       ├── auth.py            # Register, login, refresh
│       ├── users.py           # /users/me
│       ├── transactions.py    # CRUD + filters + pagination
│       ├── categories.py      # CRUD
│       ├── budgets.py         # CRUD + spending calculation
│       ├── dashboard.py       # Summary, charts data
│       ├── imports.py         # CSV/Excel upload
│       └── admin.py           # Admin-only routes
├── core/
│   ├── config.py              # Pydantic Settings (env-based)
│   ├── security.py            # JWT helpers, password hashing
│   └── deps.py                # FastAPI dependencies (auth guards)
├── db/
│   ├── base.py                # DeclarativeBase + model imports
│   └── session.py             # Engine + SessionLocal
├── models/                    # SQLAlchemy ORM models
├── schemas/                   # Pydantic request/response schemas
├── services/
│   ├── budget_service.py      # Budget spending & alert logic
│   └── import_service.py      # CSV/Excel parsing & bulk insert
├── tests/
│   ├── conftest.py            # Fixtures (test DB, client, auth headers)
│   ├── test_auth.py
│   ├── test_transactions.py
│   └── test_budgets.py
└── main.py                    # App factory, middlewares, router include
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit POSTGRES_* and SECRET_KEY

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Environment Variables

| Variable                       | Description                        | Default              |
|--------------------------------|------------------------------------|----------------------|
| `SECRET_KEY`                   | JWT signing key (generate with openssl) | —               |
| `POSTGRES_SERVER`              | DB host                            | `localhost`          |
| `POSTGRES_USER`                | DB user                            | `budgix`             |
| `POSTGRES_PASSWORD`            | DB password                        | `budgix_secret`      |
| `POSTGRES_DB`                  | DB name                            | `budgix`             |
| `ENVIRONMENT`                  | `development` / `staging` / `production` | `development` |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | JWT access token TTL               | `30`                 |
| `REFRESH_TOKEN_EXPIRE_DAYS`    | JWT refresh token TTL              | `7`                  |
| `CORS_ORIGINS`                 | Allowed origins (JSON array)       | `["http://localhost:5173"]` |

## Running Tests

```bash
# Full test suite with coverage
pytest app/tests/ -v --cov=app --cov-report=term-missing

# Single file
pytest app/tests/test_auth.py -v
```

Tests use a separate `budgix_test` database and rebuild the schema automatically via fixtures.

## Migrations

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "add column X to table Y"

# Apply all pending migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Show current revision
alembic current
```

## Docker

```bash
# Build
docker build -t budgix-backend .

# Run
docker run -p 8000:8000 --env-file .env budgix-backend
```

The Dockerfile uses a two-stage build (builder + runtime) with a non-root user for security.
