# coding=utf-8
from typing import Optional

from ultros.core.networks.base.networks.base import BaseNetwork
from ultros.networks.irc.connectors.plain import PlainConnector
from ultros.networks.irc.servers.irc import IRCServer

__author__ = "Gareth Coles"


class IRCNetwork(BaseNetwork):
    type = "irc"

    def create_server(self, name: str, *args, **kwargs):
        server = IRCServer(name, self)

        self._create_server(server)
        return server

    async def shutdown(self):
        await self._shutdown()

    async def setup(self):
        host = self.config["host"]
        port = self.config["port"]

        server = self.create_server(host)
        connector = self.create_connector(host, port, server=server)

        await connector.do_connect()

    def create_connector(self, *args, server=None, **kwargs):
        host, port = args[0], args[1]
        connector = PlainConnector(host, self, server, host=host, port=port)

        self._create_connector(connector, server)
        return connector
