from sqlalchemy.orm import Mapped
from datetime import date

from modules.base_entity import BaseEntity
from modules.base_entity import str_uniq


class TestEntity(BaseEntity):
    __tablename__ = "tests"

    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]

    def __repr__(self):
        return str(self)
