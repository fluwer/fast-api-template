from modules.test.entity import TestEntity
from modules.test.models import Test
from modules.base_repo import BaseRepository


class TestRepository(BaseRepository[TestEntity, Test]):
    def __init__(self, session_factory):
        super().__init__(session_factory, TestEntity, Test)
