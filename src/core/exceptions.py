from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError


def register_exceptions(app):
    # Обработка ошибок валидации запросов
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        simplified_errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"errors": simplified_errors}),
        )

    # Обработка ошибок Pydantic
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ):
        simplified_errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"errors": simplified_errors}),
        )


class EntityNotFound(HTTPException):
    def __init__(self, entity_name: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity not found. {entity_name if entity_name else ""}',
        )


class ApiExistsError(HTTPException):
    def __init__(self, entity_name: str = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Already exists. {entity_name if entity_name else ""}",
        )


class UnauthorizedError(HTTPException):
    def __init__(self, description: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized. {description if description else ""}",
        )


class ForbiddenError(HTTPException):
    def __init__(self, description: str = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden. {description if description else ""}",
        )
