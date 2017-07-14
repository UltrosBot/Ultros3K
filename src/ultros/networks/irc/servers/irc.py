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

    async def on_ready(self):
        self.connector.send_join("#Ultros-test")

    async def connector_connected(self, connector):
        self._connector = ref(connector)

    async def connector_disconnected(self, connector, exc):
        pass
