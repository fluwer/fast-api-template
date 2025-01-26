from core.exceptions import EntityNotFound

from modules.user.repo import UserRepository
from core.logger import Logger


class UserService:
    def __init__(
        self,
        repo: UserRepository,
    ):
        self.repo = repo
        self.logger = Logger.get_logger(__name__)

    async def get_user_by_id(self, user_id):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise EntityNotFound()
        return user
