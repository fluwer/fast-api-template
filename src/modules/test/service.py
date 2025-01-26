from core.logger import Logger

from core.exceptions import EntityNotFound
from core.exceptions import ApiExistsError

from modules.test.models import Test
from modules.test.models import TestUpdate
from modules.test.repo import TestRepository


class TestService:
    def __init__(self, repo: TestRepository):
        self.repo = repo
        self.logger = Logger.get_logger(__name__)

    async def add_test(self, test: Test) -> Test:
        exist_test = await self.repo.get_by_id(test.id)
        if exist_test:
            raise ApiExistsError()
        return await self.repo.create(test)

    async def get_test(self, test_id: int) -> Test:
        test = await self.repo.get_by_id(test_id)
        if not test:
            raise EntityNotFound()
        return test

    async def get_test_by_filter(self, first_name: str) -> Test:
        test = await self.repo.get_by_filter(first_name=first_name)
        if not test:
            raise EntityNotFound()
        return test

    async def get_all_tests(self) -> list[Test]:
        return await self.repo.get_all()

    async def update_test(self, test_id: int, updated_data: TestUpdate) -> Test:
        model = await self.repo.update(test_id, updated_data.dict())
        if model is None:
            raise EntityNotFound()
        return model

    async def delete_test(self, test_id: int):
        test = await self.repo.get_by_id(test_id)
        if not test:
            raise EntityNotFound()
        await self.repo.delete(test_id)
