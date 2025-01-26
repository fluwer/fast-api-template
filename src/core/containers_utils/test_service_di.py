from modules.test.service import TestService
from modules.test.repo import TestRepository


def get_test_service_di(providers, session):
    test_repository = providers.Factory(
        TestRepository,
        session_factory=session,
    )

    return providers.Singleton(
        TestService,
        repo=test_repository,
    )
