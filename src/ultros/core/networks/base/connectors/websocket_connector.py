# coding=utf-8
from abc import ABCMeta

from websockets import WebSocketClientProtocol

from ultros.core.networks.base.connectors.base import BaseConnector

__author__ = "Gareth Coles"


class WebsocketConnector(BaseConnector, WebSocketClientProtocol, metaclass=ABCMeta):
    pass
