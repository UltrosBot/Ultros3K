# coding=utf-8
from _weakref import ref

from ultros.core.networks.base.servers.base import BaseServer

__author__ = "Gareth Coles"


class IRCServer(BaseServer):
    _connector = None

    def __init__(self, name: str, network: "base_network.BaseNetwork"):
        super().__init__(name, network)

        self.server_capabilities = []

    @property
    def connector(self):
        if self._connector:
            return self._connector()
        return None

    async def connector_connected(self, connector):
        self._connector = ref(connector)
        self.connector.transport.write(b"CAP LS 302\r\n")
        self.connector.transport.write(b"NICK Testros\r\n")
        self.connector.transport.write(b"USER test 0 * :Ultros 3K\r\n")

    async def connector_disconnected(self, connector, exc):
        pass

    async def irc_UNHANDLED(self, tags, prefix, command, params):
        self.logger.debug(
            "Unhandled line: tags={} / prefix={} / command={} / params={}".format(
                repr(tags), repr(prefix), repr(command), repr(params)
            )
        )

    async def irc_PING(self, tags, prefix, command, params):
        self.connector.transport.write(b"PONG :" + params[0].encode("UTF-8") + b"\r\n")

    async def irc_CAP(self, tags, prefix, command, params):
        if params[0] == "*" and params[1] == "LS":
            if params[2] == "*":
                for cap in params[3].split(" "):
                    self.server_capabilities.append(cap)
            else:
                for cap in params[2].split(" "):
                    self.server_capabilities.append(cap)

                self.logger.debug("Capabilities: {}".format(", ".join(self.server_capabilities)))
                self.connector.transport.write(b"CAP END\r\n")

    async def irc_001(self, tags, prefix, command, params):
        self.connector.transport.write(b"JOIN #ultros-test\r\n")
