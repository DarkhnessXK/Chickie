import sys
import os
from pathlib import Path
# import asyncio
from aiopg import Connection

parent = str(Path(os.path.dirname(__file__)).parent)

sys.path.append(parent)


async def remover_schema(schema: str, connection: Connection) -> None:
    sql = f"""
    DROP SCHEMA {schema} CASCADE;
    CREATE SCHEMA {schema};
    """

    cursor = await connection.cursor()
    await cursor.execute(sql)

    cursor.close()

# asyncio.run(remover_schema('public'))
