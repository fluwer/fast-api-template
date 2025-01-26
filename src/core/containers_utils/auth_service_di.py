from modules.auth.service import AuthService
from modules.user.repo import UserRepository


def get_auth_service_di(providers, session):
    user_repository = providers.Factory(
        UserRepository,
        session_factory=session,
    )

    return providers.Singleton(
        AuthService,
        repo=user_repository,
    )
