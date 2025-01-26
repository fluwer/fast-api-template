from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from core.containers import Container
from core.containers import wire_modules

from core.exceptions import register_exceptions

from modules.routers import register_routers

from core.logger import Logger

logger = Logger.get_logger(__name__)

swagger_ui_parameters = {
    "syntaxHighlight": True,
    "syntaxHighlight.theme": "obsidian",
}
tags_metadata = [
    {
        "name": "auth",
        "description": "Операции с аутентификацией",
    },
    {
        "name": "user",
        "description": "Операции с пользователями",
    },
    {
        "name": "role",
        "description": "Операции с ролевой системой",
    },
    {
        "name": "test",
        "description": "Тестирование CRUD",
    },
    {
        "name": "другое",
        "description": "По мере поступления",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запущено")
    yield
    logger.info("Остановка приложения...")
    logger.info("Остановка движка базы данных...")
    await Container.database.engine.dispose()


def create_app() -> FastAPI:
    # Настройка приложения
    app = FastAPI(
        title="API сервиса *НАЗВАНИЕ*.",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        swagger_ui_parameters=swagger_ui_parameters,
        openapi_tags=tags_metadata,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация исключений
    register_exceptions(app)

    # Настройка DI
    container = Container()
    app.container = container
    wire_modules(container)

    # Регистрация роутеров
    register_routers(app)

    # Регистраций схем
    # TODO: вынести в отдельный модуль
    # openapi_schema = app.openapi()
    # user_schema = User.model_json_schema(ref_template="#/components/schemas/{model}")
    # openapi_schema["components"]["schemas"]["User"] = user_schema
    # app.openapi_schema = openapi_schema

    logger.info("Все модули зарегистрированы.")
    return app
