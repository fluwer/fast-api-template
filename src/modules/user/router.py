from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from core.containers import Container
from core.containers import inject_module

from core.authentification.jwt import oauth2_scheme
from core.authentification.jwt import secure

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from modules.responses import generate_responses
from core.exceptions import (
    EntityNotFound,
)

from modules.user.roles import Role
from modules.user.models import User
from modules.user.service import UserService

inject_module(__name__)
router = APIRouter(
    tags=["user"],
    prefix="/user",
)


@router.get(
    path="/me",
    name="Информация о текущем пользователе",
    description="Получение информации о текущем пользователе",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses=generate_responses(EntityNotFound),
)
@secure(roles=[Role.USER, Role.ADMIN])
@inject
async def get_me(
    user: User = Depends(oauth2_scheme),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.get_user_by_id(user.id)
