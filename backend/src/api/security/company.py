from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from config import settings as s
from src.infra.database_postgres.repository import Repository
from src.domain.models import Loja
from src.domain.services import LojaService


async def authenticate_company(
    username: str, password: str
) -> Optional[Loja]:
    """
    Autentica uma loja com base no nome de usuário e senha fornecidos.

    Args:
        username (str): O nome de usuário da loja.
        password (str): A senha da loja.

    Returns:
        Optional[Loja]: O objeto da loja autenticada ou
        None se a autenticação falhar.
    """

    def only_numbers(string: Optional[str]) -> Optional[str]:
        if string is None:
            return None

        return ''.join([n for n in string if n.isdecimal()])

    from src.infra.database_postgres.manager import DatabaseConnectionManager
    async with DatabaseConnectionManager() as connection:
        service = LojaService(connection)
        loja_repo = Repository(Loja, connection=connection)
        l1 = await loja_repo.find_one(username=username)
        l2 = await loja_repo.find_one(email=username)
        l3 = await loja_repo.find_one(celular=only_numbers(username))

        loja = l1 or l2 or l3

        if loja is None or not isinstance(loja, Loja):
            return None

        if not service.authenticate(loja=loja, senha_loja=password):
            return None

        return loja


async def current_company(
    token: str
) -> Loja:
    """
    Obtém o objeto da loja atualmente autenticada.

    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): O token de acesso JWT.

    Returns:
        Loja: O objeto da loja autenticada.

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
    except JWTError:
        raise credentials_exception

    async with DatabaseConnectionManager() as connection:
        loja_repo = Repository(Loja, connection=connection)
        loja = await loja_repo.find_one(username=username)

    if loja is None or not isinstance(loja, Loja):
        raise credentials_exception

    return loja
