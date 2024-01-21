import sys
from config import settings as s

try:
    arg = sys.argv[1]
except Exception:
    arg = "dev"

s.POSTGRES_DATABASE = arg

import asyncio  # noqa

from src.infra.database_postgres.entities import Base  # noqa
from src.infra.database_postgres.config import engine  # noqa
from src.api import ext  # noqa


async def create_database(database_name=arg or s.POSTGRES_DATABASE):
    from src.infra import database_postgres

    await database_postgres.config.init_database(database_name=database_name)
    Base.metadata.create_all(engine)


asyncio.run(create_database(arg))
# asyncio.run(ext.init_commands.init_app(sys.argv))
