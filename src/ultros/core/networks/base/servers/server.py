# coding=utf-8
from typing import Optional
from weakref import ref

from ultros.core.networks.base.connectors import base as base_connector
from ultros.core.networks.base import network as base_network

__author__ = "Gareth Coles"


class BaseServer:
    def __init__(self, network: "base_network.BaseNetwork"):
        self._network = ref(network)

    @property
    def network(self) -> "base_network.BaseNetwork":
        return self._network()

    def connector_connected(self, connector: "base_connector.BaseConnector"):
        pass

    def connector_disconnected(self, connector: "base_connector.BaseConnector",
                               exc: Optional[Exception]):
        pass
