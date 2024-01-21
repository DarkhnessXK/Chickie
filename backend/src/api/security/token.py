from datetime import datetime, timedelta
from jose import jwt
from config import settings as s


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
        expires_delta = timedelta(seconds=int(str(s.JWT_EXPIRE_TIME)))

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, s.SECRET_KEY, algorithm=s.AUTH_ALGORITHM
    )
    return encoded_jwt
