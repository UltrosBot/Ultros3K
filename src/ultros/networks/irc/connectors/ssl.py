# coding=utf-8
import asyncio

from ultros.networks.irc.connectors.base import BaseIRCConnector

__author__ = "Gareth Coles"


class SSLIRCConnector(BaseIRCConnector):
    async def do_connect(self):
        transport, _ = await asyncio.get_event_loop().create_connection(lambda: self, self.host, self.port, ssl=True)
