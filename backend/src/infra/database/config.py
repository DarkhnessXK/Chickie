from sqlalchemy.engine import create_engine
from config import settings as s
from src.infra.database.manager import DatabaseConnectionManager
from sqlalchemy.orm.session import sessionmaker
from time import sleep


database_url = "{0}+{1}://{2}:{3}@{4}/{5}".format(
    "postgresql",
    "psycopg2",
    s.POSTGRES_USERNAME,
    s.POSTGRES_PASSWORD,
    s.POSTGRES_HOST,
    s.POSTGRES_DATABASE_DEV,
)

engine = create_engine(database_url)


async def init_database():
    # await DatabaseConnectionManager.create_database(
    #     name=s.POSTGRES_DATABASE_PROD
    # )
    await DatabaseConnectionManager.create_database(
        name=s.POSTGRES_DATABASE_DEV
    )


def get_db():
    while True:
        try:
            Session = sessionmaker(engine)
            return Session()
        except Exception:
            sleep(5)
