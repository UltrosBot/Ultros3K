# coding=utf-8

"""
Base class to be inherited by all networks
"""

from abc import ABCMeta, abstractmethod
from typing import Optional, Set

from ultros.core.networks.base.connectors import base as base_connector
from ultros.core.networks.base.servers import base as base_server
from ultros.core.storage.config.base import ConfigFile

__author__ = "Gareth Coles"


class BaseNetwork(metaclass=ABCMeta):
    type = "base"  #: str: The type of network, eg "irc"

    def __init__(self, name: str, config: ConfigFile):
        self.name = name
        self.config = config

        self.config.set_owner(self)

        self._servers = {}  #: Dict[str, BaseServer]
        self._connectors = {}  #: Dict[str, BaseConnector]

        self._connector_associations = {}  #: Dict[str, List[BaseConnector]]

    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def shutdown(self):
        pass

    async def _shutdown(self):
        for _, server in self._servers:
            self.destroy_server(server)

    def notify_connected(self, connector: "base_connector.BaseConnector"):
        server = self.get_server_for_connector(connector)

        if not server:
            return  # TODO: Logging

        try:
            server.connector_connected(connector)
        except Exception as e:
            pass  # TODO: Logging

    def notify_disconnected(self, connector: "base_connector.BaseConnector",
                            exc: Optional[Exception]):
        server = self.get_server_for_connector(connector)

        if not server:
            return  # TODO: Logging

        try:
            server.connector_disconnected(connector, exc)
        except Exception as e:
            pass  # TODO: Logging

    def get_server_for_connector(self, connector: "base_connector.BaseConnector") \
            -> Optional["base_server.BaseServer"]:
        for server_name, connector_list in self._connector_associations.items():
            if connector in connector_list and self.has_server(server_name):
                return self.get_server(server_name)

    def has_server(self, server: str) -> bool:
        return server in self._servers

    def get_server(self, server: str) -> Optional["base_server.BaseServer"]:
        return self._servers.get(server)

    @abstractmethod
    async def create_server(self, name: str, *args, **kwargs) -> "base_server.BaseServer":
        pass

    def _create_server(self, server: "base_server.BaseServer"):
        self._servers[server.name] = server

    async def destroy_server(self, server: "base_server.BaseServer"):
        connectors = self._connector_associations[server.name]

        for connector in connectors:
            await self.destroy_connector(connector, remove_association=False)

        del self._servers[server.name]
        del self._connector_associations[server.name]

    @abstractmethod
    async def create_connector(self, *args,
                               server: Optional["base_server.BaseServer"]=None,
                               **kwargs) -> "base_connector.BaseConnector":
        pass

    def _create_connector(self, connector: "base_connector.BaseConnector",
                          server: Optional["base_server.BaseServer"]=None):
        self._connectors[connector.name] = connector

        if server:
            self._connector_associations[server.name] = connector

    async def destroy_connector(self, connector: "base_connector.BaseConnector", remove_association=True):
        try:
            await connector.disconnect()
        except Exception as e:
            pass  # TODO: Logging

        del self._connectors[connector.name]

        if remove_association:
            for server_name, connectors in self._connector_associations:
                if connector in connectors:
                    connectors.remove(connector)
