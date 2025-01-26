from sqlalchemy.orm import Mapped

from modules.base_entity import BaseEntity
from modules.base_entity import str_null_true
from modules.base_entity import str_null_false
from modules.base_entity import str_uniq


class UserEntity(BaseEntity):
    __tablename__ = "users"

    email: Mapped[str_uniq]
    password: Mapped[str_null_false]
    user_name: Mapped[str_null_true]
    role: Mapped[str_null_false]

    def __repr__(self):
        return str(self)
