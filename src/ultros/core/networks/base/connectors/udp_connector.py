# coding=utf-8
from abc import ABCMeta
from asyncio import DatagramProtocol

from ultros.core.networks.base.connectors.base import BaseConnector

__author__ = "Gareth Coles"


class UDPConnector(BaseConnector, DatagramProtocol, metaclass=ABCMeta):
    pass
