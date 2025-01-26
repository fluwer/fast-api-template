from modules.base_pydantic import BasePydanticModel


class Token(BasePydanticModel):
    access_token: str
    refresh_token: str


class UserLogin(BasePydanticModel):
    username: str
    password: str
