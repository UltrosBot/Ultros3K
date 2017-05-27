# coding=utf-8
import asyncio
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase

from sqlalchemy import Table, Column, Integer, String, MetaData, inspect, select
from sqlalchemy.sql.ddl import CreateTable

from ultros.core.storage.database.sqla import SQLADatabase
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestSQLA(TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        self.directory = os.path.join(tempfile.gettempdir(), secrets.token_urlsafe(10))

        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        self.config_dir = os.path.join(self.directory, "config")
        self.data_dir = os.path.join(self.directory, "data")

        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        self.manager = StorageManager(
            ultros=None,
            config_location=self.config_dir,
            data_location=self.data_dir
        )

    def tearDown(self):
        self.manager.shutdown()
        del self.manager

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

    def test_sqlite(self):
        """
        Test SQLAlchemy integration using a simple SQLite database
        """

        results = {}

        def _database_obj() -> SQLADatabase:
            db_path = os.path.join(self.directory, "test.db")
            return self.manager.get_database(
                "sqlite:///{}".format(db_path)
            )

        database = _database_obj()

        users = Table(
            "users", database.metadata,
            Column("id", Integer(), primary_key=True),
            Column("name", String())
        )

        async def do_create_table():
            results["create_table"] = False
            await database.execute(CreateTable(users))

            results["create_table"] = True

        async def do_insert():
            results["insert"] = False

            connection = await database.get_connection()

            await connection.execute(users.insert().values(name="Gareth Coles"))
            await connection.execute(users.insert().values(name="Sean Gordon"))
            await connection.execute(users.insert().values(name="John Madden"))
            await connection.execute(users.insert().values(name="Pepe LePew"))
            await connection.execute(users.insert().values(name="Fluttershy"))

            result = await connection.execute(users.select(users.c.name.startswith("G")))
            d_users = await result.fetchall()

            await connection.close()

            for user in d_users:
                if user[users.c.name] == "Gareth Coles":
                    results["insert"] = True

        async def do_context_manager():
            results["context_manager"] = False

            async with database.get_connection() as conn:
                async with conn.begin() as _:  # Transaction
                    r = await conn.execute(select([1]))
                    d = await r.fetchone()

                    if d == (1,):
                        results["context_manager"] = True

        self.loop.run_until_complete(do_create_table())
        self.loop.run_until_complete(do_insert())
        self.loop.run_until_complete(do_context_manager())

        assert_true(
            results["create_table"], "Table creation not executed"
        )
        assert_true(
            results["insert"], "Data was not inserted"
        )
        assert_true(
            results["context_manager"], "Context manager didn't fetch scalar"
        )
