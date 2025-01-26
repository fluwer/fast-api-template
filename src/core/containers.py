from typing import Set

from dependency_injector import containers
from dependency_injector import providers

from core.containers_utils.base import get_di_config
from core.containers_utils.base import get_database

from core.containers_utils.auth_service_di import get_auth_service_di
from core.containers_utils.user_service_di import get_user_service_di
from core.containers_utils.test_service_di import get_test_service_di

modules: Set = set()


class Container(containers.DeclarativeContainer):
    config = get_di_config()
    database = get_database(providers)

    auth_service = get_auth_service_di(
        providers=providers,
        session=database.provided.session,
    )

    user_service = get_user_service_di(
        providers=providers,
        session=database.provided.session,
    )

    test_service = get_test_service_di(
        providers=providers,
        session=database.provided.session,
    )


def inject_module(module_name: str):
    modules.add(module_name)


def wire_modules(container):
    container.wire(modules=list(modules))
