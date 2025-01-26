from functools import wraps

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import ForbiddenError

from core.containers import Container
from core.containers import inject_module

from jose import jwt
from jose import JWTError

from typing import Optional
from typing import Annotated

from core.config import get_config
from core.logger import logger

from modules.user.models import User
from modules.user.roles import Role
from modules.user.service import UserService

inject_module(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login_swagger")
config = get_config()


def secure(roles: list[Role] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            **kwargs,
        ):
            jwt_token = kwargs.get("user")

            user = await _get_user(jwt_token)

            if roles and user.role not in [role.value for role in roles]:
                raise ForbiddenError(f"Insufficient permissions")

            kwargs["user"] = user
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@inject
async def _get_user(
    jwt_token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Provide[Container.user_service],
) -> Optional[User]:
    payload = await valid_token(jwt_token)
    user_id: int = payload.get("user_id")
    user = await user_service.repo.get_by_id(user_id)
    logger.info("Fetched user: %s", user)
    return user


async def valid_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        if payload.get("token_type") != "access":
            raise ForbiddenError(f"Invalid or expired token")
        return payload
    except JWTError:
        raise ForbiddenError("Invalid or expired token")
