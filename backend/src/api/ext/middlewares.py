import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import time
from src.misc import ConsoleColors as CC
import logging
from aiopg import Pool


def init_app(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_process_time_header(  # noqa
        request: Request,
        call_next
    ) -> Response:
        now = datetime.datetime.now().isoformat()
        t1 = time.perf_counter()
        response: Response = await call_next(request)
        t2 = time.perf_counter()
        Δt = t2 - t1
        response.headers['x-request-process-time'] = f'{round(Δt*1000, 2)}ms'
        response.headers['x-request-datetime'] = now

        return response

    @app.middleware("http")
    async def database_connection_middleware(
        request: Request,
        call_next
    ) -> Response:
        app: FastAPI = request.app
        pool: Pool = app.state.connection_pool

        async with pool.acquire() as connection:
            request.state.connection = connection

            conn = '...' + str(id(request.state.connection))[-5:]

            msg = f'...Got connection: {conn}'
            logging.debug(CC.warning(msg))
            response: Response = await call_next(request)
            # await request.state.connection.close()

            # msg = f'Closed connection: {conn}'
            # logging.debug(CC.okgreen(msg))

        return response

    @app.get('/teste')
    async def teste():
        return {'msg': 'ok'}
