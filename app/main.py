from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router as router

app = FastAPI(
    title="Subscription Management API",
    version="0.1.0",
)

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

register_exception_handlers(app)
app.include_router(router)
