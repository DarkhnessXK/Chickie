from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from config import settings as s
from src.infra.database_postgres.repository import Repository
from src.domain.models import Loja, Usuario
from src.domain.services import LojaService
from aiopg import Connection
import datetime


class AuthService:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, connection: Connection):
        self.connection = connection
        self.loja_service = LojaService(self.connection)
        self.loja_repo = Repository(Loja, connection=self.connection)
        self.user_repo = Repository(Usuario, connection=self.connection)

    async def authenticate_company(
        self,
        username: str,
        password: str
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

        l1 = await self.loja_repo.find_one(username=username)
        l2 = await self.loja_repo.find_one(email=username)
        l3 = await self.loja_repo.find_one(celular=self.only_numbers(username))
        loja = l1 or l2 or l3

        if loja is None or not isinstance(loja, Loja):
            return None

        if not self.loja_service.authenticate(loja=loja, senha_loja=password):
            return None

        return loja

    async def authenticate_user(
        self, username: str,
        password: str
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

        u1 = await self.user_repo.find_one(username=username)
        u2 = await self.user_repo.find_one(email=username)
        u3 = await self.user_repo.find_one(celular=self.only_numbers(username))
        user = u1 or u2 or u3

        if user is None or not isinstance(user, Usuario):
            return None

        if not user.authenticate(password):
            return None

        return user

    async def current_company(self, token: str) -> Loja:
        """
        Obtém o objeto da loja atualmente autenticada.

        Args:
            token (str): O token de acesso JWT.

        Returns:
            Loja: O objeto da loja autenticada.

        Raises:
            HTTPException: Se a autenticação falhar.
        """
        try:
            payload = jwt.decode(
                token, s.SECRET_KEY, algorithms=[s.AUTH_ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise AuthService.credentials_exception
        except JWTError:
            raise AuthService.credentials_exception

        loja = await self.loja_repo.find_one(username=username)

        if loja is None or not isinstance(loja, Loja):
            raise AuthService.credentials_exception

        return loja

    async def current_user(self, token: str) -> Usuario:
        """
        Obtém o objeto do usuário atualmente autenticado.

        Args:
            token (str): O token de acesso JWT.

        Returns:
            Usuario: O objeto do usuário autenticado.

        Raises:
            HTTPException: Se a autenticação falhar.
        """

        try:
            payload = jwt.decode(
                token, s.SECRET_KEY, algorithms=[s.AUTH_ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise self.credentials_exception
        except JWTError:
            raise self.credentials_exception

        user = await self.user_repo.find_one(username=username)

        if user is None or not isinstance(user, Usuario):
            raise AuthService.credentials_exception

        return user

    def only_numbers(self, string: Optional[str]) -> Optional[str]:
        if string is None:
            return None
        return ''.join([n for n in string if n.isdecimal()])

    @classmethod
    def create_access_token(
        cls,
        data: dict,
        expires_delta: datetime.timedelta | None = None
    ):
        """
        Cria um token de acesso JWT com os dados fornecidos.

        Args:
            data (dict): Os dados a serem codificados no token.
            expires_delta (timedelta | None, optional): A duração de
            validade do token. Se None, será usado o tempo padrão.

        Returns:
            str: O token de acesso JWT.
        """
        to_encode = data.copy()
        if expires_delta is None:
            expires_delta = datetime.timedelta(
                seconds=int(str(s.JWT_EXPIRE_TIME))
            )

        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, s.SECRET_KEY, algorithm=s.AUTH_ALGORITHM
        )
        return encoded_jwt
