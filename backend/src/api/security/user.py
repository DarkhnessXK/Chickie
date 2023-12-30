from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from config import settings as s
from src.infra.database_postgres.repository import Repository
from src.infra.database_postgres.manager import DatabaseConnectionManager
from src.schemas import TokenData, Usuario
from src.api.security.scheme import oauth2_scheme


async def authenticate_user(
    username: str, password: str
) -> Optional[Usuario]:
    """
    Autentica um usuário com base no nome de usuário e senha fornecidos.

    Args:
        username (str): O nome de usuário do usuário.
        password (str): A senha do usuário.

    Returns:
        Optional[Usuario]: O objeto do usuário autenticado
        ou None se a autenticação falhar.
    """
    async with DatabaseConnectionManager() as connection:
        user_repo = Repository(Usuario, connection=connection)
        user = await user_repo.find_one(username=username)

        if user is None or not isinstance(user, Usuario):
            return None

        if not user.authenticate(password):
            return None

        return user


async def current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Usuario:
    """
    Obtém o objeto do usuário atualmente autenticado.

    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): O token de acesso JWT.

    Returns:
        Usuario: O objeto do usuário autenticado.

    Raises:
        HTTPException: Se a autenticação falhar.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, s.SECRET_KEY, algorithms=[s.AUTH_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    async with DatabaseConnectionManager() as connection:
        user_repo = Repository(Usuario, connection=connection)
        user = await user_repo.find_one(username=token_data.username)

    if user is None or not isinstance(user, Usuario):
        raise credentials_exception

    return user
