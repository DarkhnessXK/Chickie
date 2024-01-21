from fastapi import FastAPI


def create_app(args: list) -> FastAPI:

    app = FastAPI()

    from src.api import routes
    from src.api import ext

    routes.init_app(app)
    ext.config.init_app(app)
    ext.middlewares.init_app(app)
    ext.events.init_app(app)
    ext.logging.init_app(app)

    return app
