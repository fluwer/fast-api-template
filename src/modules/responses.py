from typing import Type

from fastapi import status, HTTPException

responses = {
    status.HTTP_200_OK: {"description": "OK"},
    status.HTTP_201_CREATED: {"description": "Created"},
    status.HTTP_204_NO_CONTENT: {"description": "No Content"},
    status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    status.HTTP_402_PAYMENT_REQUIRED: {"description": "Payment Required"},
    status.HTTP_403_FORBIDDEN: {"description": "Not enough privileges"},
    status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    status.HTTP_409_CONFLICT: {"description": "Conflict"},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Unprocessable Entity"},
}


def generate_responses(*exceptions: Type[HTTPException]) -> dict[int, dict]:
    """
    Генерирует словарь `responses` для FastAPI на основе исключений.

    :param exceptions: Список исключений.
    :return: Словарь с кодами статусов и описаниями.
    """
    _responses = {
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable Entity.",
            "content": {
                "application/json": {"example": {"detail": "Validation failed. "}}
            },
        }
    }

    for exc in exceptions:
        exc_instance = exc()
        _responses[exc_instance.status_code] = {
            "description": exc_instance.detail,
            "content": {
                "application/json": {"example": {"detail": exc_instance.detail}}
            },
        }
    return _responses
