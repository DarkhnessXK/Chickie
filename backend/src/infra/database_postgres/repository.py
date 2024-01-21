from aiopg import Connection
import logging
from uuid import uuid4
from typing import List, Optional, Any
from asyncio import Lock
from src.misc import ConsoleColors


class Repository:
    """A generic repository class to interact with a database table
    for a Pydantic model."""

    def __init__(self, model: Any, connection: Connection):
        """Initialize the repository.

        Args:
            model (Any): The Pydantic model representing the database table.
            connection (Connection): The aiopg database connection.
        Example:
            repository = Repository(Endereco, connection=connection)
            try:
                itens_removed = await repository.delete_from_uuid(
                    uuid=uuid
                )
            except Exception as error:
                raise HTTPException(status_code=500, detail=str(error))
        """
        self.lock = Lock()
        self.model = model
        self.connection = connection
        self.columns = list(model.model_fields.keys())  # type: ignore
        self.tablename: str = model.__tablename__  # type: ignore

    async def find_one(self, **kwargs) -> Optional[Any]:
        """Find a single row in the database table based on given criteria.

        Args:
            **kwargs: Keyword arguments representing the filtering criteria.

        Returns:
            Optional[Any]: The Pydantic model instance
            representing the row if found, None otherwise.
        """
        values = None
        result = None
        if kwargs:
            columns = list(kwargs.keys())
            values = list(kwargs.values())
            where_clause = " AND ".join([f"{c} = %s" for c in columns])
            query = f"SELECT * FROM {self.tablename} WHERE {where_clause};"

        else:
            query = f"SELECT * FROM {self.tablename}"

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(query, values)
            result = await cursor.fetchone()

        logging.debug(
            ConsoleColors.okblue(
                f"\n\nQuery: {query} Values: {values}\n\n"
            )
        )

        if result:
            column_names = []
            if cursor.description is not None:
                for item in cursor.description:
                    column_names.append(item[0])

            dict_result = dict(list(zip(column_names, result)))
            cursor.close()

            return self.model(**dict_result)  # type: ignore

        cursor.close()
        return None

    async def find_all(self, **kwargs) -> List[Any]:
        """Find all rows in the database table based on given criteria.

        Args:
            **kwargs: Keyword arguments representing the filtering criteria.

        Returns:
            List[Any]: A list of Pydantic model instances
            representing the rows.
        """
        values = None
        if kwargs:
            columns = list(kwargs.keys())
            values = list(kwargs.values())
            where_clause = " AND ".join([f"{c} = %s" for c in columns])
            query = "SELECT * FROM {} WHERE {};".format(
                self.tablename, where_clause
            )
        else:
            query = f"SELECT * FROM {self.tablename}"

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(query, values)
            results = await cursor.fetchall()

        logging.debug(
            ConsoleColors.okblue(
                f"\n\nQuery: {query} Values: {values}\n\n"
            )
        )

        column_names = []
        if cursor.description is not None:
            for item in cursor.description:
                column_names.append(item[0])

        response_dicts = [
            {key: value for key, value in zip(column_names, list(result))}
            for result in results
        ]

        response = [self.model(**item) for item in response_dicts if item]

        cursor.close()
        return response

    async def find_all_cointaining(self, **kwargs) -> List[Any]:
        """Find all rows in the database table containing the given values.

        Args:
            **kwargs: Keyword arguments representing the values to be searched.

        Returns:
            List[Any]: A list of Pydantic model instances
            representing the rows.
        """
        if kwargs == {}:
            raise KeyError("Method must have at least one key to search")

        columns = list(kwargs.keys())
        values = list(kwargs.values())

        where_clause = " AND ".join([f"{c} LIKE %s" for c in columns])

        query = f"SELECT * FROM {self.tablename} WHERE {where_clause};"
        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(query, [f"%{value}%" for value in values])
            results = await cursor.fetchall()

        logging.debug(
            ConsoleColors.okblue(
                f"\n\nQuery: {query} Values: {values}\n\n"
            )
        )

        column_names = []
        if cursor.description is not None:
            for item in cursor.description:
                column_names.append(item[0])

        response_dicts = [
            {key: value for key, value in zip(column_names, list(result))}
            for result in results
        ]
        response = [self.model(**item) for item in response_dicts if item]

        cursor.close()
        return response

    async def save(self, model: Any) -> str:
        """Save a new row in the database table.

        Args:
            model (Any): The Pydantic model instance
                representing the row to be saved.

        Returns:
            str: The UUID of the saved row.
        """
        kwargs = model.model_dump()  # type: ignore
        kwargs["uuid"] = str(uuid4())

        columns = list(kwargs.keys())
        values = list(kwargs.values())

        column_clause = ", ".join(columns)
        value_placeholder = ", ".join(["%s"] * len(columns))

        command = "INSERT INTO {} ({}) VALUES ({});".format(
            self.tablename, column_clause, value_placeholder
        )

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(command, values)

        cursor.close()

        logging.debug(
            ConsoleColors.okgreen(
                f"\n\nCommand: {command} Values: {values}\n\n"
            )
        )
        return kwargs["uuid"]

    async def update(self, item: Any, data: dict = {}) -> int:
        """Update an existing row in the database table.

        Args:
            item (Any): The Pydantic model instance
                representing the row to be updated.

            data (dict, optional): The data to be updated.
                Defaults to an empty dictionary.

        Returns:
            int: The number of rows affected by the update operation.
        """
        values = list(data.values())

        set_clause = ", ".join([f"{column} = %s" for column in data.keys()])
        command = "UPDATE {} SET {} WHERE uuid = '{}';".format(
            self.tablename, set_clause, item.uuid
        )
        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(command, values)

        num_rows_affected = cursor.rowcount

        cursor.close()
        logging.debug(
            ConsoleColors.okgreen(
                f"\n\nCommand: {command} Values: {values}\n\n"
            )
        )
        return num_rows_affected

    async def delete(self, item: Any) -> int:
        """Delete an existing row from the database table.

        Args:
            item (Any): The Pydantic model instance
            representing the row to be deleted.

        Returns:
            int: The number of rows affected by the delete operation.
        """
        uuid = item.uuid
        command = f"DELETE FROM {self.tablename} WHERE uuid = %s;"

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(command, (uuid,))

        num_rows_affected = cursor.rowcount

        cursor.close()
        logging.debug(
            ConsoleColors.fail(
                f"\n\nCommand: {command} uuid = {uuid}\n\n"
            )
        )
        return num_rows_affected

    async def delete_from_uuid(self, uuid) -> int:
        """Delete an existing row from the database table based on its UUID.

        Args:
            uuid: The UUID of the row to be deleted.

        Returns:
            int: The number of rows affected by the delete operation.
        """
        command = f"DELETE FROM {self.tablename} WHERE uuid = %s;"

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(command, (uuid,))

        num_rows_affected = cursor.rowcount

        cursor.close()
        logging.debug(
            ConsoleColors.fail(
                f"\n\nCommand: {command} uuid = {uuid}\n\n"
            )
        )
        return num_rows_affected

    async def execute_and_fetch_one(self, query: str, params: tuple):
        """ """
        logging.debug(
            ConsoleColors.okblue(
                f"\n\nCommand: {query}\n\n"
            )
        )

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(query, params)

        column_names = []
        if cursor.description is not None:
            for item in cursor.description:
                column_names.append(item[0])

        result = await cursor.fetchone()

        if result:
            column_names = []
            if cursor.description is not None:
                for item in cursor.description:
                    column_names.append(item[0])

            dict_result = dict(list(zip(column_names, result)))
            cursor.close()
            return dict_result

        cursor.close()
        return None

    async def execute_and_fetch_all(self, query: str, params: tuple):
        """ """
        logging.debug(
            ConsoleColors.okblue(
                f"Query: {query}"
            )
        )

        async with self.lock:
            cursor = await self.connection.cursor()
            await cursor.execute(query, params)

        column_names = []
        if cursor.description is not None:
            for item in cursor.description:
                column_names.append(item[0])

        results = await cursor.fetchall()

        response_dicts = [
            {key: value for key, value in zip(column_names, list(result))}
            for result in results
        ]

        cursor.close()
        return response_dicts
