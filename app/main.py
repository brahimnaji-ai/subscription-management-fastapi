from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router as router

app = FastAPI(
    title="Subscription Management API",
    version="0.1.0",
)

register_exception_handlers(app)
app.include_router(router)
