from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, categories, transactions, budgets, dashboard, imports, admin

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(categories.router)
api_router.include_router(transactions.router)
api_router.include_router(budgets.router)
api_router.include_router(dashboard.router)
api_router.include_router(imports.router)
api_router.include_router(admin.router)
