from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.domain import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
    PlanAlreadyExistsException,
    PlanNotFoundException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PlanAlreadyExistsException)
    async def handle_plan_already_exists(
        request: Request,
        exc: PlanAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PlanNotFoundException)
    async def handle_plan_not_found(
        request: Request,
        exc: PlanNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )


    @app.exception_handler(CustomerAlreadyExistsException)
    async def handle_customer_already_exists(
            request: Request,
            exc: CustomerAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CustomerNotFoundException)
    async def handle_customer_not_found(
            request: Request,
            exc: CustomerNotFoundException ,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )
