from fastapi import FastAPI

from app.api.router import api_router as router

app = FastAPI(
    title="Subscription Management API",
    version="0.1.0",
)

app.include_router(router)
