# coding=utf-8
from abc import ABCMeta
from asyncio import SubprocessProtocol

from ultros.core.networks.base.connectors.base import BaseConnector

__author__ = "Gareth Coles"


class ProcessConnector(BaseConnector, SubprocessProtocol, metaclass=ABCMeta):
    pass
