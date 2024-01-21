from config import settings as s
from fastapi import FastAPI
from aiopg import create_pool, Pool, Connection
from src.misc import ConsoleColors as CC
import logging


def init_app(app: FastAPI):

    @app.on_event('startup')
    async def startup() -> None:

        async def on_pool_connect(connection: Connection):
            try:
                app.state.connections
            except AttributeError:
                app.state.connections = set()

            conn_id = str(id(connection))[-5:]
            msg = f'on_connect: Got connection ...{conn_id}'
            app.state.connections.add('...' + conn_id)
            logging.warning(CC.warning(msg))
            msg = CC.warning(str({'Connections': app.state.connections}))
            logging.warning(CC.warning(msg))

        app.state.connection_pool = await create_pool(
            ("dbname={0} user={1} password={2} host={3}".format(
                s.POSTGRES_DATABASE,
                s.POSTGRES_USERNAME,
                s.POSTGRES_PASSWORD,
                s.POSTGRES_HOST,
            )),
            maxsize=5,
            minsize=5,
            echo=True,
            on_connect=on_pool_connect
        )
        app.state.connection_pool.echo
        print(f'Created pool {app.state.connection_pool}')

    @app.on_event('shutdown')
    async def shutdown() -> None:
        pool: Pool = app.state.connection_pool
        print(f'Got pool {pool}')
        pool.close()
        await pool.wait_closed()
        print('Finalizando...')
        print(f'Closed pool {pool}')
