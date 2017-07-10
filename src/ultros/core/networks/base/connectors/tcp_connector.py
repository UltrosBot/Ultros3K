# coding=utf-8
from abc import ABCMeta
from asyncio import Protocol

from ultros.core.networks.base.connectors.base import BaseConnector

__author__ = "Gareth Coles"


class TCPConnector(BaseConnector, Protocol, metaclass=ABCMeta):
    pass
