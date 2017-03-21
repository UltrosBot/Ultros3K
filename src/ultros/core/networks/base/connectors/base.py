# coding=utf-8
from abc import ABCMeta
from asyncio import BaseTransport
from typing import Optional

from ultros.core.networks.base import network as base_network

from weakref import ref

__author__ = "Gareth Coles"


class BaseConnector(metaclass=ABCMeta):
    transport = None  #: BaseTransport

    def __init__(self, network: "base_network.BaseNetwork"):
        self._network = ref(network)

    @property
    def network(self) -> "base_network.BaseNetwork":
        return self._network()

    def connection_made(self, transport: BaseTransport):
        self.transport = transport
        self.network.notify_connected(self)

    def connection_lost(self, exc: Optional[Exception]):
        self.network.notify_disconnected(self, exc)
