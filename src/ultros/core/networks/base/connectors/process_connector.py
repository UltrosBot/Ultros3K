# coding=utf-8
from abc import ABCMeta
from asyncio import SubprocessProtocol

__author__ = "Gareth Coles"


class ProcessConnector(SubprocessProtocol, metaclass=ABCMeta):
    pass
