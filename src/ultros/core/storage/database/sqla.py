# coding=utf-8
"""
SQLAlchemy-based class for relational databases, powered by SQLAlchemy-AIO
"""

from typing import Any, List, Dict, Coroutine
from ultros.core.storage.database.base import RelationalDatabase

from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import MetaData, create_engine

__author__ = "Gareth Coles"


class SQLADatabase(RelationalDatabase):
    """
    SQLAlchemy-based class for relational databases, powered by SQLAlchemy-AIO

    This is an asyncio-powered SQLAlchemy wrapper with a very light API. We used `sqlalchemy_aio` under the hood; more
    documentation on that can be found here: https://github.com/RazerM/sqlalchemy_aio

    Note that this abstraction means that you can't use the ORM. If an ORM is really required, we will create
    another API wrapper for you - but note that it will not be asynchronous and may end up blocking
    some of your functions and overall harming the responsiveness of Ultros as a result. Raise a ticket if you
    want to look into this further.

    Example usage:

    >>> db = ultros.storage_manager.get_database(
    ...     "sqlite:///{}".format(os.path.join(ultros.storage_manager.data_location, "test.db"))
    ... )
    >>> users = Table(
    ...     "users", db.metadata,
    ...     Column("id", Integer(), primary_key=True),
    ...     Column("name", String())
    ... )
    >>> async def some_function():
    ...     db.execute(CreateTable(users))
    ...     with db.get_connection() as conn:
    ...         await conn.execute(users.insert().values(name="Pippi"))
    ...         await conn.execute(users.insert().values(name="Hatsune Miku"))
    ...         result = await conn.execute(users.select(user.c.name.startswith("H")))
    ...         d_users = result.fetchall()
    ...     for user in d_users:
    ...         logger.info("User: {}".format(user[users.c.name]))
    >>>

    For more information on this, you can check out the SQLAlchemy documentation, the documentation for
    `sqlalchemy_aio`, or our unit tests.
    """

    def __init__(self, owner: Any, manager, url: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, url, *args, **kwargs)

        self.engine = None
        self.metadata = None

    def load(self):
        self.engine = create_engine(
            self._url, strategy=ASYNCIO_STRATEGY
        )

        self.metadata = MetaData()

    def unload(self):
        self.engine.dispose()
        self.metadata.clear()

        self.engine = None
        self.metadata = None

    async def execute(self, *args, **kwargs):
        """
        Wrapper for `engine.execute()`
        """

        return await self.engine.execute(*args, **kwargs)

    def get_connection(self) -> Coroutine:
        """
        Return a coroutine that will result in a new connection
        """

        return self.engine.connect()
