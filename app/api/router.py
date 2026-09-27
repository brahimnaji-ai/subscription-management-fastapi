from fastapi import APIRouter

from app.api.v1.customer_router import router as customer_router
from app.api.v1.plan_router import router as plan_router
from app.api.v1.subscription_router import router as subscription_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(plan_router)
api_router.include_router(customer_router)
api_router.include_router(subscription_router)
