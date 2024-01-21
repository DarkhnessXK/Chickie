from src.infra.database_postgres.repository import Repository
from src.domain.models import (
    Usuario,
    UsuarioSignUp,
    EnderecoUsuario as Endereco
)
from aiopg import Connection
from src.api.security import HashService
from src.exceptions import InvalidPasswordException
from typing import Optional


def validate_password(password: Optional[str]) -> bool:
    if password is None:
        return False
    if len(password) < 6:
        return False

    return True


async def registrar(
    user_data: UsuarioSignUp,
    connection: Connection
) -> Usuario:

    valid = validate_password(user_data.password)
    if not valid:
        raise InvalidPasswordException
    user_repo = Repository(Usuario, connection=connection)

    def only_numbers(string: str | None) -> str:
        if string is None:
            return ''
        return ''.join([n for n in string if n.isdecimal()])

    user = Usuario(
        nome=user_data.nome,
        username=user_data.username,
        email=user_data.email,
        celular=only_numbers(user_data.celular),
        telefone=only_numbers(user_data.telefone),
        modo_de_cadastro=user_data.modo_de_cadastro,
        password_hash=HashService.hash(password=user_data.password),
    )
    del user.password
    user.uuid = await user_repo.save(model=user)
    endereco = Endereco(
        uf=user_data.uf,
        cidade=user_data.cidade,
        logradouro=user_data.logradouro,
        numero=user_data.numero,
        bairro=user_data.bairro,
        cep=user_data.cep,
        complemento=user_data.complemento,
        usuario_uuid=user.uuid
    )
    endereco_repository = Repository(Endereco, connection=connection)
    await endereco_repository.save(endereco)
    del user_data
    return user
