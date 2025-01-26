from modules.user.service import UserService
from modules.user.repo import UserRepository


def get_user_service_di(providers, session):
    user_repository = providers.Factory(
        UserRepository,
        session_factory=session,
    )

    return providers.Singleton(
        UserService,
        repo=user_repository,
    )
