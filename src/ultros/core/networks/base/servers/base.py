# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Optional
from weakref import ref

from ultros.core.networks.base.connectors import base as base_connector
from ultros.core.networks.base.networks import base as base_network

__author__ = "Gareth Coles"


class BaseServer(metaclass=ABCMeta):
    def __init__(self, name: str, network: "base_network.BaseNetwork"):
        self.name = name
        self._network = ref(network)

    @property
    def network(self) -> "base_network.BaseNetwork":
        return self._network()

    @abstractmethod
    async def connector_connected(self, connector: "base_connector.BaseConnector"):
        pass

    @abstractmethod
    async def connector_disconnected(self, connector: "base_connector.BaseConnector",
                                     exc: Optional[Exception]):
        pass
