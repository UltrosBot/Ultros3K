# coding=utf-8
from abc import ABCMeta, abstractmethod
from asyncio import BaseTransport, BaseProtocol
from typing import Optional
from weakref import ref

from ultros.core.networks.base.networks import base as base_network
from ultros.core.networks.base.servers import base as base_server

__author__ = "Gareth Coles"


class BaseConnector(BaseProtocol, metaclass=ABCMeta):
    transport = None  #: BaseTransport

    def __init__(self, name: str, network: "base_network.BaseNetwork", server: "base_server.BaseServer"):
        self.name = name

        if server:
            self._server = ref(server)

        self._network = ref(network)

    @property
    def network(self) -> "base_network.BaseNetwork":
        return self._network()

    @property
    def server(self) -> "base_server.BaseServer":
        return self._server()

    def set_server(self, server: "base_server.BaseServer"):
        self._server = ref(server)

    @abstractmethod
    async def do_connect(self):
        pass

    @abstractmethod
    async def do_disconnect(self):
        pass

    def connection_made(self, transport):
        super().connection_made(transport)

        self.transport = transport
        self.network.notify_connected(self)

    def connection_lost(self, exc):
        super().connection_lost(exc)

        self.network.notify_disconnected(self, exc)
