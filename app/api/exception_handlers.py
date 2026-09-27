from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.domain import (
    CustomerAlreadyExistsException,
    CustomerAlreadySubscribedException,
    CustomerNotFoundException,
    InvalidSubscriptionStateException,
    PlanAlreadyExistsException,
    PlanInactiveException,
    PlanNotFoundException,
    SamePlanChangeException,
    SubscriptionNotFoundException,
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

    @app.exception_handler(PlanInactiveException)
    async def handle_plan_inactive(
        request: Request,
        exc: PlanInactiveException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
        exc: CustomerNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CustomerAlreadySubscribedException)
    async def handle_customer_already_subscribed(
        request: Request,
        exc: CustomerAlreadySubscribedException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(SubscriptionNotFoundException)
    async def handle_subscription_not_found(
        request: Request,
        exc: SubscriptionNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidSubscriptionStateException)
    async def handle_invalid_subscription_state(
        request: Request,
        exc: InvalidSubscriptionStateException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)},
        )

    @app.exception_handler(SamePlanChangeException)
    async def handle_same_plan_change(
        request: Request,
        exc: SamePlanChangeException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

