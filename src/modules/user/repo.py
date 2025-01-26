from typing import Optional

from sqlalchemy import select

from modules.user.entity import UserEntity
from modules.user.models import User

from modules.base_repo import BaseRepository


class UserRepository(BaseRepository[UserEntity, User]):
    def __init__(self, session_factory):
        super().__init__(session_factory, UserEntity, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(self.entity).where(self.entity.email == email)
            result = await session.execute(query)
            entity = result.scalar()
            return self.to_model(entity) if entity else None
