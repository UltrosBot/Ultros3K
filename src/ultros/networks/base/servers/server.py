# coding=utf-8
from typing import Optional
from weakref import ref

from ultros.networks.base.connectors.base import BaseConnector
from ultros.networks.base.network import BaseNetwork

__author__ = "Gareth Coles"


class BaseServer:
    def __init__(self, network: BaseNetwork):
        self._network = ref(network)

    @property
    def network(self) -> BaseNetwork:
        return self._network()

    def connector_connected(self, connector: BaseConnector):
        pass

    def connector_disconnected(self, connector: BaseConnector,
                               exc: Optional[Exception]):
        pass
