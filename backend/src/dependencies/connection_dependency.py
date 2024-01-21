from aiopg import Connection
from typing import Annotated
from fastapi import (  # noqa
    Depends,
    Request
)


def get_connection(request: Request):
    return request.state.connection


ConnectionDependency = Annotated[Connection, Depends(get_connection)]  # noqa
