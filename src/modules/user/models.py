from typing import Optional
from typing import Annotated

from pydantic import EmailStr
from pydantic import Field

from modules.base_pydantic import BasePydanticModel
from modules.user.roles import Role


class User(BasePydanticModel):
    id: Annotated[
        int,
        Field(
            None,
            description="ID пользователя",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Электронная почта пользователя",
        ),
    ]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Пароль пользователя",
            exclude=True,
        ),
    ]
    role: Annotated[
        str,
        Field(
            Role.USER,
            description="Роль пользователя",
        ),
    ]
    user_name: Optional[str] = Field(
        None,
        description="Имя пользователя",
    )


class UserCreate(BasePydanticModel):
    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Электронная почта пользователя",
        ),
    ]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Пароль пользователя",
        ),
    ]
