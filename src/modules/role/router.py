from dependency_injector.wiring import inject
from core.containers import inject_module

from fastapi import APIRouter
from fastapi import status

from modules.user.roles import Role

inject_module(__name__)
router = APIRouter(
    tags=["role"],
    prefix="/role",
)


@router.get(
    path="/roles/",
    name="Список ролей",
    description="Список ролей",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
@inject
async def get_all_roles():
    return [role.value for role in Role]
