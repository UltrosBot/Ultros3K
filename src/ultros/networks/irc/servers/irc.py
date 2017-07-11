# coding=utf-8
from _weakref import ref

from ultros.core.networks.base.servers.base import BaseServer

__author__ = "Gareth Coles"


class IRCServer(BaseServer):
    _connector = None

    @property
    def connector(self):
        if self._connector:
            return self._connector()
        return None

    async def connector_connected(self, connector):
        self._connector = ref(connector)
        connector.transport.write(b"NICK Test\r\n")
        connector.transport.write(b"USER test 0 * :Ultros\r\n")

    async def connector_disconnected(self, connector, exc):
        pass

    async def irc_UNHANDLED(self, tags, prefix, command, params):
        self.logger.debug(
            "Line: tags={} / prefix={} / command={} / params={}".format(
                repr(tags), repr(prefix), repr(command), repr(params)
            )
        )

    async def irc_PING(self, tags, prefix, command, params):
        self.connector.transport.write(b"PONG :" + params[0].encode("UTF-8") + b"\r\n")
        self.connector.transport.write(b"JOIN #ultros\r\n")
