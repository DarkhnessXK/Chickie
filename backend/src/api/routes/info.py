from fastapi import FastAPI
from src.misc import get_project_info


def init_app(app: FastAPI) -> None:

    info = get_project_info()

    @app.get("/")
    async def index():
        """
        Rota para obter informações sobre o aplicativo e as rotas disponíveis.

        Retorna um JSON contendo informações sobre a versão,
        nome e descrição do aplicativo,
        bem como links para as rotas disponíveis e detalhes sobre as ações
        (rotas) do aplicativo.
        """
        return {
            "version": info['version'],
            "name": info['name'],
            "description": info['description'],
            "authors": info['authors'],
            "links": [
                {"rel": "self", "href": "http://localhost:8000/"},
            ]
            + [
                {
                    "rel": route.path.split("/")[1],  # type: ignore
                    "href": route.path,  # type: ignore
                }
                for route in app.router.routes
                if route.path != "/"  # type: ignore
            ],
            "actions": [
                {
                    "name": (
                        route.name.replace(  # type: ignore
                            "_", " "
                        ).capitalize()
                    ),
                    "methods": list(route.methods),  # type: ignore
                    "path": route.path,  # type: ignore
                }
                for route in app.router.routes  # type: ignore
            ],
        }

    @app.get("/favicon.ico")
    async def favicon():
        """
        Rota para servir o favicon do aplicativo.

        Retorna uma resposta vazia (b"").
        """
        return b""
