# coding=utf-8
from abc import ABCMeta
from asyncio import DatagramProtocol

__author__ = "Gareth Coles"


class UDPConnector(DatagramProtocol, metaclass=ABCMeta):
    pass
