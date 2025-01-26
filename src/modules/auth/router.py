from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from typing import Annotated

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.containers import Container
from core.containers import inject_module

from modules.responses import generate_responses
from core.exceptions import (
    ApiExistsError,
    UnauthorizedError,
    ForbiddenError,
)

from modules.auth.service import AuthService

from modules.auth.models import Token, UserLogin
from modules.user.models import User
from modules.user.models import UserCreate

inject_module(__name__)
router = APIRouter(
    tags=["auth"],
    prefix="/auth",
)


@router.post(
    path="/register",
    name="Регистрация пользователя",
    description="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    responses=generate_responses(ApiExistsError),
)
@inject
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.register(user)


@router.post(
    path="/login_swagger",
    name="Авторизация пользователя (SWAGGER)",
    description="Авторизация пользователя (SWAGGER)",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses=generate_responses(UnauthorizedError),
)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    token = await auth_service.authenticate(form_data.username, form_data.password)
    return token


@router.post(
    path="/login",
    name="Авторизация пользователя",
    description="Авторизация пользователя",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses=generate_responses(UnauthorizedError),
)
@inject
async def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    token = await auth_service.authenticate(login_data.username, login_data.password)
    return token


@router.post(
    path="/refresh",
    name="Обновление access токена",
    description="Обновление access токена с помощью refresh токена",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses=generate_responses(ForbiddenError, UnauthorizedError),
)
@inject
async def refresh(
    refresh_token: str,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    token = await auth_service.refresh_access_token(refresh_token)
    return token
