from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.misc import get_project_info


def init_app(app: FastAPI):

    info = get_project_info()

    if app.openapi_schema:
        return app.openapi_schema

    app.openapi_schema = get_openapi(
        title=info['name'],
        version=info['version'],
        description=info['description'],
        routes=app.routes  # noqa
    )
