from datetime import datetime
from datetime import timedelta

from jose import jwt
from jose import JWTError
from passlib.context import CryptContext

from core.exceptions import ApiExistsError
from core.exceptions import ForbiddenError
from core.exceptions import UnauthorizedError

from core.config import get_config
from core.logger import Logger
from modules.auth.models import Token

from modules.user.models import UserCreate, User
from modules.user.repo import UserRepository
from modules.user.roles import Role


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
    ):
        self.repo = repo
        self.config = get_config()
        self.logger = Logger.get_logger(__name__)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, user: UserCreate) -> User:
        """
        Регистрация нового пользователя.
        """
        email = user.email.lower()
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ApiExistsError(f"User with email {existing_user.email}")

        hashed_password = self.pwd_context.hash(user.password)

        new_user: User = User(
            email=user.email,
            password=hashed_password,
            role=Role.USER,
        )
        return await self.repo.create(new_user)

    async def authenticate(self, email: str, password: str) -> Token:
        """
        Аутентификация пользователя.
        """
        user = await self.repo.get_by_email(email)
        if not user or not self.pwd_context.verify(password, user.password):
            raise UnauthorizedError("Invalid credentials")

        access_token = self.create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "user_role": user.role,
            }
        )
        refresh_token = self.create_refresh_token(
            data={"sub": user.email, "user_id": user.id}
        )
        token: Token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        return token

    def create_access_token(
        self,
        data: dict,
    ) -> str:
        """
        Создание токена доступа (access token).
        """
        encode = data.copy()
        encode["token_type"] = "access"
        expires = datetime.now() + timedelta(
            minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        encode.update({"exp": expires.timestamp()})

        jwt_encoded = jwt.encode(
            encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM
        )

        return jwt_encoded

    def create_refresh_token(
        self,
        data: dict,
    ) -> str:
        """
        Создание токена обновления (refresh token).
        """
        encode = data.copy()
        encode["token_type"] = "refresh"
        expires = datetime.now() + timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS)
        encode.update({"exp": expires.timestamp()})

        jwt_encoded = jwt.encode(
            encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM
        )

        return jwt_encoded

    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Обновление токена доступа по токену обновления.
        """
        try:
            payload = jwt.decode(
                refresh_token,
                self.config.SECRET_KEY,
                algorithms=[self.config.ALGORITHM],
            )
            if payload["token_type"] == "access":
                raise ForbiddenError("Invalid or expired token")

            user_id: int = payload.get("user_id")
            user = await self.repo.get_by_id(user_id)
            if not user:
                raise UnauthorizedError("User not found")

            access_token = self.create_access_token(
                data={
                    "sub": user.email,
                    "user_id": user.id,
                    "user_role": user.role,
                }
            )
            new_refresh_token = self.create_refresh_token(
                data={"user_id": user.id, "sub": user.email}
            )
            token: Token = Token(
                access_token=access_token,
                refresh_token=new_refresh_token,
            )
            return token
        except JWTError:
            raise ForbiddenError("Invalid or expired token")
