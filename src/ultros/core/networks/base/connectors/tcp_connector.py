# coding=utf-8
from abc import ABCMeta
from asyncio import Protocol

__author__ = "Gareth Coles"


class TCPConnector(Protocol, metaclass=ABCMeta):
    pass
