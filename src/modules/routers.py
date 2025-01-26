from core.containers import inject_module

from modules.auth.router import router as auth_router
from modules.role.router import router as role_router
from modules.user.router import router as user_router
from modules.test.router import router as test_router

inject_module(__name__)

# Общий список роутеров
ALL_ROUTERS = [
    auth_router,
    role_router,
    user_router,
    test_router,
]


def register_routers(app):
    for rout in ALL_ROUTERS:
        app.include_router(rout, prefix="/api")
