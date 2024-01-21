from src.domain.models import Loja
from typing import Annotated
from fastapi import (  # noqa
    Depends
)
from .service_dependencies import AuthServiceDependency
from .token_dependency import TokenDependency


async def get_current_loja(
    auth_service: AuthServiceDependency,
    token: TokenDependency
):
    return await auth_service.current_company(token)

CurrentLojaDependency = Annotated[Loja, Depends(get_current_loja)]
