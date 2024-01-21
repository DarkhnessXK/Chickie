from typing import Any, Annotated, Optional
from src.exceptions import UnauthorizedException
from fastapi import (
    HTTPException,
    status,
    Response,
    Depends
)
from src.misc import Paginador  # noqa
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.exceptions import NotFoundException
from src.infra.database_postgres.repository import Repository
from src.api.security import AuthService, oauth2_scheme
from src.domain.models import (
    UsuarioFollowEmpresaRequest,
    UsuarioSignUp,
    EnderecoUsuario as Endereco,
    Usuario,
    Cliente,
    ClientePOST,
    UserAuthData,
)
from src import use_cases
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/user", tags=["Usuario"])


@router.post("/login", response_model=UserAuthData, tags=["Auth"])
async def login_post(
    connection: ConnectionDependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:

    endereco_repository = Repository(Endereco, connection=connection)
    auth_service = AuthService(connection)

    user = await auth_service.authenticate_user(
        form_data.username, form_data.password
    )

    if not user:
        raise UnauthorizedException("Credenciais Inválidas!")

    access_token = AuthService.create_access_token({"sub": user.username})
    endereco: Optional[Endereco] = await endereco_repository.find_one(
        usuario_uuid=user.uuid
    )

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


@router.post("/signup", status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def signup(
    connection: ConnectionDependency,
    usuario: UsuarioSignUp
) -> Any:

    try:
        usuario_uuid = await use_cases.usuarios.registrar(
            user_data=usuario,
            connection=connection
        )
    except use_cases.usuarios.InvalidPasswordException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Senha inválida! A senha deve ser maior que 5"
        )

    return {"uuid": usuario_uuid}


@router.put("/{uuid}")
async def update_user(
    connection: ConnectionDependency,
    uuid: str,
    user_data: UsuarioSignUp,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Any:
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    endereco_repository = Repository(Endereco, connection)
    user_repository = Repository(Endereco, connection)

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


@router.post("/seguir-loja")
async def seguir_loja(
    connection: ConnectionDependency,
    response: Response,
    token: Annotated[str, Depends(oauth2_scheme)],
    follow_request_data: UsuarioFollowEmpresaRequest
) -> Any:
    result: str | int
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    cliente = ClientePOST(
        usuario_uuid=follow_request_data.usuario_uuid,
        loja_uuid=follow_request_data.loja_uuid
    )

    cliente_repository = Repository(Cliente, connection=connection)

    if follow_request_data.follow:
        response.status_code = 201
        result = await cliente_repository.save(cliente)
        return {"result": result, 'follow': follow_request_data.follow}

    else:
        relationship: Optional[Cliente] = await cliente_repository.find_one(
            usuario_uuid=follow_request_data.usuario_uuid,
            loja_uuid=follow_request_data.loja_uuid
        )

        if relationship:
            result = await cliente_repository.delete(relationship)
            return {'result': result, 'follow': follow_request_data.follow}

    return {'result': None, 'follow': follow_request_data.follow}


@router.get("/segue-loja/{uuid}")
async def segue_loja(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: str
) -> Any:

    auth_service = AuthService(connection)
    current_user = await auth_service.current_user(token)
    if current_user.uuid is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Usuario sem uuid'
        )

    cliente_repository = Repository(Cliente, connection=connection)
    follows: Optional[Cliente] = await cliente_repository.find_one(
        usuario_uuid=current_user.uuid,
        loja_uuid=uuid
    )
    if follows:
        return {'result': True}

    else:
        return {'result': False}
