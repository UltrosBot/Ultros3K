# coding=utf-8
from typing import Optional, Set

from ultros.networks.base.connectors.base import BaseConnector
from ultros.networks.base.servers.server import BaseServer

__author__ = "Gareth Coles"


class BaseNetwork:
    def __init__(self):
        self._servers = {}  #: Dict[str, BaseServer]
        self._connectors = []  #: List[BaseConnector]
        self._connector_associations = {}  #: Dict[str, List[BaseConnector]]

    def notify_connected(self, connector: BaseConnector):
        for server in self.get_servers_for_connector(connector):
            try:
                server.connector_connected(connector)
            except Exception as e:
                continue  # TODO: Logging

    def notify_disconnected(self, connector: BaseConnector,
                            exc: Optional[Exception]):
        for server in self.get_servers_for_connector(connector):
            try:
                server.connector_disconnected(connector, exc)
            except Exception as e:
                continue  # TODO: Logging

    def get_servers_for_connector(self, connector: BaseConnector) \
            -> Set[BaseServer]:
        servers = set()

        for server_name, connector_list in self._connector_associations.items():
            if connector in connector_list and self.has_server(server_name):
                servers.add(self.get_server(server_name))

        return servers

    def has_server(self, server: str) -> bool:
        return server in self._servers

    def get_server(self, server: str) -> Optional[BaseServer]:
        return self._servers.get(server)
