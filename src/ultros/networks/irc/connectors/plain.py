# coding=utf-8
import asyncio

from ultros.core.networks.base.connectors.tcp_connector import TCPConnector

__author__ = "Gareth Coles"


class PlainConnector(TCPConnector):
    def __init__(self, name: str, network, server, *, host=None, port=6667):
        super().__init__(name, network, server)

        self.host = host
        self.port = port
        self.buffer = b""

    async def do_connect(self):
        transport, _ = await asyncio.get_event_loop().create_connection(lambda: self, self.host, self.port)

    async def do_disconnect(self):
        self.transport.close()

    def data_received(self, data: bytes):
        self.buffer += data

        while b"\r\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\r\n", 1)

            try:
                parsed = self.parse_line(line.decode("UTF-8"))  # TODO: Encoding
            except Exception:
                self.logger.exception("Failed to parse line")
                self.logger.error(line)
            else:
                self.logger.debug(line)
                asyncio.ensure_future(self.dispatch_line(parsed))

    def eof_received(self):
        return False  # Closes the transport automatically

    async def dispatch_line(self, data: dict):
        function_name = "irc_{}".format(data["command"])
        if not hasattr(self.server, function_name):
            function_name = "irc_UNHANDLED"
        await getattr(self.server, function_name)(**data)

    def parse_line(self, line) -> dict:
        # TODO: There's probably a lot of validation I missed
        data = {
            "tags": {},
            "prefix": None,
            "command": None,
            "params": []
        }

        if line[0] == "@":
            tags, line = line.split(" ", 1)

            for tag in tags.split(";"):
                if "=" in tag:
                    key, value = tag.split("=", 1)
                else:
                    key, value = tag, None

                if key not in data["tags"]:
                    data["tags"][key] = value

        if line[0] == ":":
            prefix, line = line.split(" ", 1)
            data["prefix"] = prefix[1:]

        command, line = line.split(" ", 1)
        data["command"] = command.upper()

        while line:  # Params to do!
            if " " in line:
                param, line = line.split(" ", 1)
            else:
                param, line = line, ""

            if param[0] == ":":
                data["params"].append(param[1:] + " " + line)
                break

            data["params"].append(param)

        return data
