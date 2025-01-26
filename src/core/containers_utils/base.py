from database.database import Database
from core.config import get_config


def get_di_config():
    return get_config()


def get_database(providers):
    return providers.Singleton(
        Database,
    )
