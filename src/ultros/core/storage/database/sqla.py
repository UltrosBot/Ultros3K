# coding=utf-8
from typing import Any, List, Dict, Coroutine
from ultros.core.storage.database.base import RelationalDatabase

from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import MetaData, create_engine

__author__ = "Gareth Coles"


class SQLADatabase(RelationalDatabase):
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
        return await self.engine.execute(*args, **kwargs)

    def get_connection(self) -> Coroutine:
        return self.engine.connect()
