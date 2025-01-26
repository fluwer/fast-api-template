import re
from typing import Annotated

from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

from datetime import date
from datetime import datetime

from modules.base_pydantic import BasePydanticModel


class TestBase(BasePydanticModel):
    phone_number: Annotated[
        str,
        Field(
            default=...,
            description="Номер телефона в международном формате, начинающийся с '+'",
        ),
    ]
    first_name: Annotated[
        str,
        Field(
            default=...,
            min_length=1,
            max_length=50,
            description="Имя студента, от 1 до 50 символов",
        ),
    ]
    date_of_birth: Annotated[
        date,
        Field(
            default=...,
            description="Дата рождения студента в формате ГГГГ-ММ-ДД",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            default=...,
            description="Электронная почта студента",
        ),
    ]

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values


class Test(TestBase):
    id: Annotated[
        int,
        Field(
            default=...,
            description="ID студента",
        ),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "phone_number": "+1234567890",
                "first_name": "Иван",
                "date_of_birth": "2000-01-01",
                "email": "ivan@example.com",
            }
        }


class TestUpdate(TestBase):
    pass
