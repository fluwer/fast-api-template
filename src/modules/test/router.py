from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from core.containers import Container
from core.containers import inject_module

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from modules.responses import generate_responses
from core.exceptions import (
    ApiExistsError,
    EntityNotFound,
)

from modules.test.service import TestService
from modules.test.models import Test
from modules.test.models import TestUpdate

inject_module(__name__)
router = APIRouter(
    tags=["test"],
    prefix="/test",
)


@router.post(
    path="/tests/",
    name="Новый тест",
    description="Новый тест",
    status_code=status.HTTP_201_CREATED,
    response_model=Test,
    responses=generate_responses(ApiExistsError),
)
@inject
async def create_test(
    test: Test,
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    return await test_service.add_test(test)


@router.get(
    path="/tests/{test_id}",
    name="Получает тест",
    description="Получает тест",
    status_code=status.HTTP_200_OK,
    response_model=Test,
    responses=generate_responses(EntityNotFound),
)
@inject
async def get_test(
    test_id: int,
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    return await test_service.get_test(test_id)


@router.get(
    path="/tests/",
    name="Получает список всех тестов",
    description="Получает список всех тестов",
    status_code=status.HTTP_200_OK,
    response_model=list[Test],
)
@inject
async def get_all_tests(
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    return await test_service.get_all_tests()


@router.put(
    path="/tests/{test_id}",
    name="Обновляет тест по ID",
    description="Обновляет тест по ID",
    status_code=status.HTTP_201_CREATED,
    response_model=Test,
    response_model_exclude=None,
    responses=generate_responses(EntityNotFound),
)
@inject
async def update_test(
    test_id: int,
    test: TestUpdate,
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    return await test_service.update_test(test_id, test)


@router.delete(
    path="/tests/{test_id}",
    name="Удаляет тест по ID",
    description="Удаляет тест по ID",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses=generate_responses(EntityNotFound),
)
@inject
async def delete_test(
    test_id: int,
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    await test_service.delete_test(test_id)
    return


@router.get(
    path="/tests/filter/{test_id}",
    name="Получает тест по фильтру",
    description="Получает тест по фильтру",
    status_code=status.HTTP_200_OK,
    response_model=Test,
    responses=generate_responses(EntityNotFound),
)
@inject
async def get_by_filter(
    first_name: str,
    test_service: TestService = Depends(Provide[Container.test_service]),
):
    return await test_service.get_test_by_filter(first_name)
