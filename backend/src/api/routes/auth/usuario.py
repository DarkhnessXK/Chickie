from typing import Any, Annotated, Optional
from src.exceptions import UnauthorizedException
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from src.exceptions import NotFoundException
from src.infra.database_postgres.repository import Repository
from src.api import security
from src.schemas import (
    UsuarioFollowEmpresaRequest,
    UsuarioSignUp,
    EnderecoUsuario as Endereco,
    Usuario,
    Cliente,
    Token,
)
from src import use_cases
from src.dependencies import (
    current_user,
    endereco_repository_dependency,
    usuario_repository_dependency,
    connection_dependency
)


router = APIRouter(prefix="/user", tags=["Usuario", "Auth"])


@router.post("/login", response_model=Token)
async def login_post(
    request: Request,
    connection: connection_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    """
    Realiza o login de um usuário.

    Args:
        request (Request): O objeto de requisição HTTP.
        form_data (OAuth2PasswordRequestForm): Dados do formulário de login.

    Returns:
        dict: Um dicionário contendo o token de acesso e o uuid do usuário.

    Raises:
        HTTPException: Se as credenciais forem inválidas.
    """
    endereco_repository = Repository(Endereco, connection=connection)

    user = await security.authenticate_user(
        form_data.username, form_data.password
    )

    if not user:
        raise UnauthorizedException("Credenciais Inválidas!")

    endereco: Optional[Endereco] = await endereco_repository.find_one(
        usuario_uuid=user.uuid
    )

    access_token = security.create_access_token(data={"sub": user.username})

    response = {
        "access_token": access_token,
        "token_type": "bearer",
        "uuid": user.uuid,
        "nome": user.nome,
        "username": user.username,
        "email": user.email,
        "celular": user.celular
    }

    if endereco:
        response['endereco'] = endereco

    return response


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(usuario: UsuarioSignUp) -> Any:
    """
    Realiza o cadastro de um novo usuário.

    Args:
        usuario (UsuarioSignUp): Os detalhes do usuário a ser cadastrado.

    Returns:
        dict: Um dicionário contendo o uuid do usuário cadastrado.
    """
    try:
        usuario_uuid = await use_cases.usuarios.registrar(user_data=usuario)
    except use_cases.usuarios.InvalidPasswordException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Senha inválida! A senha deve ser maior que 5"
        )

    return {"uuid": usuario_uuid}


@router.get("/protected")
async def home(current_user: current_user):
    """
    Rota de exemplo protegida por autenticação.

    Args:
        current_user (Usuario): O objeto do usuário autenticado.

    Returns:
        dict: Uma mensagem de resposta.
    """
    return {"msg": "ok"}


@router.put("/{uuid}")
async def update_user(
    uuid: str,
    user_data: UsuarioSignUp,
    current_user: current_user,
    user_repository: usuario_repository_dependency,
    endereco_repository: endereco_repository_dependency
) -> Any:
    """
    Atualiza os detalhes de um usuário existente.

    Args:
        user_uuid (str): O UUID do usuário a ser atualizado.
        user_data (UsuarioSignUp): Os novos detalhes do usuário.
        current_user (Usuario): O objeto do usuário autenticado.

    Returns:
        dict: Um dicionário vazio.
    """

    usuario: Optional[Usuario] = await user_repository.find_one(uuid=uuid)
    if usuario is None or usuario.uuid is None:
        raise NotFoundException('Usuario não encontrado')

    def only_numbers(string: str | None) -> str | None:
        if string is None:
            return None

        return ''.join([n for n in string if n.isdecimal()])

    try:
        usuario_updated_data = dict(
            nome=user_data.nome,
            username=user_data.username,
            email=user_data.email,
            celular=only_numbers(user_data.celular),
            telefone=only_numbers(user_data.telefone),
            password_hash=usuario.password_hash,
        )

        success = await user_repository.update(
            usuario, usuario_updated_data
        )

        novo_endereco = Endereco(
            uf=user_data.uf,
            cidade=user_data.cidade,
            logradouro=user_data.logradouro,
            numero=user_data.numero,
            bairro=user_data.bairro,
            complemento=user_data.complemento,
            usuario_uuid=usuario.uuid
        )
        endereco: Optional[Endereco] = await endereco_repository.find_one(
            usuario_uuid=usuario.uuid
        )
        if endereco:
            await endereco_repository.delete(endereco)

        endereco_uuid = await endereco_repository.save(novo_endereco)

        return {
            "message": "Usuario atualizado com sucesso!",
            "uuid": usuario.uuid,
            'endereco_uuid': endereco_uuid,
            "success": success
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar dados de usuario! Detalhes: {error}"
        )


@router.post("/cliente", status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente(
    connection: connection_dependency,
    current_user: current_user,
    usuario: UsuarioFollowEmpresaRequest
) -> Any:
    """
    Cadastra um novo cliente associado à loja autenticada.

    Args:
        current_company (Loja): O objeto da loja autenticada.
        usuario (UsuarioSignUp): Os detalhes do cliente a ser cadastrado.

    Returns:
        dict: Um dicionário contendo o uuid do usuário (cliente) cadastrado.

    Raises:
        HTTPException: Se não for fornecido o uuid da loja.
    """
    if usuario.loja_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="uuid da loja em falta",
        )

    cliente = Cliente(
        usuario_uuid=usuario.usuario_uuid,
        loja_uuid=usuario.loja_uuid
    )

    cliente_repository = Repository(Cliente, connection=connection)
    cliente_uuid = await cliente_repository.save(cliente)

    return {"uuid": cliente_uuid}
