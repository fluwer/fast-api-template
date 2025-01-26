from src.core.config import get_config
from src.core.server import create_app

if __name__ == "__main__":
    import uvicorn

    app = create_app()
    config = get_config()

    uvicorn.run(
        app,
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=False,
        workers=1,
    )
