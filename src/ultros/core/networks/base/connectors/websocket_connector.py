# coding=utf-8
from abc import ABCMeta

from websockets import WebSocketClientProtocol

__author__ = "Gareth Coles"


class WebsocketConnector(WebSocketClientProtocol, metaclass=ABCMeta):
    pass
