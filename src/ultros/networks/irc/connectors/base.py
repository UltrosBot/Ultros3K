# coding=utf-8
import asyncio

from ultros.core.networks.base.connectors.tcp_connector import TCPConnector
from ultros.networks.irc.servers import irc as irc_server

__author__ = "Gareth Coles"


class BaseIRCConnector(TCPConnector):
    def __init__(self, name: str, network, server, *, host=None, port=6667, encoding="UTF-8"):
        super().__init__(name, network, server)

        self.host = host
        self.port = port
        self.encoding = encoding

        self.server_capabilities = []
        self.supported_features = {}

        self.buffer = b""

    @property
    def server(self) -> "irc_server.IRCServer":
        return self._server()

    def connection_made(self, transport):
        super().connection_made(transport)

        self.write_line("CAP LS 302")
        self.write_line("NICK Testros")
        self.write_line("USER test 0 * :Ultros 3K")

    async def do_disconnect(self):
        self.transport.close()

    def write_line(self, line):
        bytes_line = line.encode(self.encoding)
        self.transport.write(
            bytes_line + b"\r\n"
        )

        self.logger.debug("-> {}".format(repr(bytes_line)))

    def data_received(self, data: bytes):
        self.buffer += data

        while b"\r\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\r\n", 1)

            try:
                parsed = self.parse_line(line.decode(self.encoding))
            except Exception:
                self.logger.exception("Failed to parse line")
                self.logger.error(line)
            else:
                self.logger.debug("<- {}".format(repr(line)))
                asyncio.ensure_future(self.dispatch_line(parsed))

    def eof_received(self):
        return False  # Closes the transport automatically

    async def dispatch_line(self, data: dict):
        function_name = "irc_{}".format(data["command"])
        if not hasattr(self, function_name):
            function_name = "irc_UNHANDLED"
        await getattr(self, function_name)(**data)

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

    # region: Non-numerics

    async def irc_UNHANDLED(self, tags, prefix, command, params):
        self.logger.debug(
            "Unhandled line: tags={} / prefix={} / command={} / params={}".format(
                repr(tags), repr(prefix), repr(command), repr(params)
            )
        )

    async def irc_PING(self, tags, prefix, command, params):
        self.write_line("PONG :{}".format(params[0]))

    async def irc_CAP(self, tags, prefix, command, params):
        if params[0] == "*" and params[1] == "LS":
            if params[2] == "*":
                for cap in params[3].split(" "):
                    self.server_capabilities.append(cap)
            else:
                for cap in params[2].split(" "):
                    self.server_capabilities.append(cap)

                self.logger.debug("Capabilities: {}".format(", ".join(self.server_capabilities)))
                self.write_line("CAP END")

    # endregion

    # region: Numerics

    async def irc_001(self, tags, prefix, command, params):
        """
        RPL_WELCOME
        """

        if len(params) > 1:
            self.logger.info(params[1])
        elif params:
            self.logger.info(params[0])
        else:
            self.logger.info("Received WELCOME message.")

        await self.server.on_ready()
        # self.write_line("JOIN #ultros-test")

    async def irc_002(self, tags, prefix, command, params):
        """
        RPL_YOURHOST
        """

        if len(params) > 1:
            self.logger.info(params[1])
        elif params:
            self.logger.info(params[0])

    async def irc_003(self, tags, prefix, command, params):
        """
        RPL_CREATED
        """

        if len(params) > 1:
            self.logger.info(params[1])
        elif params:
            self.logger.info(params[0])

    async def irc_004(self, tags, prefix, command, params):
        """
        RPL_MYINFO

        We should use RPL_ISUPPORT (005) to discover features instead of using the mode letters listed here
        """

        server_name = params[1]
        server_version = params[2]
        user_modes = params[3]
        chanel_modes = params[4]

        if len(params) > 5:
            channel_modes_with_parameter = params[5]
        else:
            channel_modes_with_parameter = ""

    async def irc_005(self, tags, prefix, command, params):
        """
        RPL_ISUPPORT

        Possible parameters include the following...

        AWAYLEN=<number>
        CASEMAPPING=<ascii/rfc1459/rfc7613>
        CHANLIMIT=<prefixes>:[limit]{,<prefixes>:[limit], ...}
        CHANMODES=<mode>[,<mode> ...]
        CHANELLEN=<number>
        CHANTYPES=[type][type ...]                                  default: "#"
        ELIST=<extension>[extension ...]
        EXCEPTS=[character]                                         default: "e"
        EXTBAN=[<prefix>],<types>
        INVEX=[character]                                           default: "I"
        KICKLEN=<number>
        MAXLIST=<modes>:<limit>{,<modes>:<limit> ...}
        MAXTARGETS=[number]                                         default: No limit
        MODES=[number]                                              default: No limit
        NETWORK=<string>
        NICKLEN=<number>
        PREFIX=[(modes)prefixes]                                    default: "(ov)@+"
        SAFELIST
        SILENCE=[limit]                                             default: Command not supported
        STATUSMSG=<prefix>[prefix ...]
        TARGMAX=[<command>:[limit]{,<command>:[limit] ...}]
        TOPICLEN=<number>
        """

        params = params[1:-1]

        for param in params:
            if "=" in param:
                left, right = param.split("=", 1)

                if left[0] == "-":
                    left = left[1:]

                    if left in self.supported_features:
                        del self.supported_features[left]

                    continue

                if "," in right:
                    self.supported_features[left] = right.split(",")
                    continue

                self.supported_features[left] = [right]
                continue

            self.supported_features[param] = [None]

    async def irc_010(self, tags, prefix, command, params):
        """
        RPL_BOUNCE

        Not recommended that servers use this as implementations differ and it doesn't specify whether to use SSL.
        We should think about whether we implement this, and if so, how.
        """

        hostname, port, info = params[1, 2, 3:]

    async def irc_221(self, tags, prefix, command, params):
        """
        RPL_UMODEIS
        """

        umodes = params[1]

    async def irc_250(self, tags, prefix, command, params):
        """
        Unknown numeric, used by Esper
        """

        self.logger.info(params[1])

    async def irc_251(self, tags, prefix, command, params):
        """
        RPL_LUSERCLIENT
        """

        self.logger.info(params[1])

    async def irc_252(self, tags, prefix, command, params):
        """
        RPL_LUSEROP
        """

        self.logger.info(" ".join(params[1:]))

    async def irc_253(self, tags, prefix, command, params):
        """
        RPL_LUSERUNKNOWN
        """

        self.logger.info(" ".join(params[1:]))

    async def irc_254(self, tags, prefix, command, params):
        """
        RPL_LUSERCHANNELS
        """

        self.logger.info(" ".join(params[1:]))

    async def irc_255(self, tags, prefix, command, params):
        """
        RPL_LUSERME
        """

        self.logger.info(params[1])

    async def irc_256(self, tags, prefix, command, params):
        """
        RPL_ADMINME
        """

        if len(params) > 2:  # Server can be specified, but it's in the prefix anyway
            self.logger.info(params[2])
        else:
            self.logger.info(params[1])

        self.logger.info(" ".join(params[1:]))

    async def irc_257(self, tags, prefix, command, params):
        """
        RPL_ADMINLOC1
        """

        self.logger.info(params[1])

    async def irc_258(self, tags, prefix, command, params):
        """
        RPL_ADMINLOC2
        """

        self.logger.info(params[1])

    async def irc_259(self, tags, prefix, command, params):
        """
        RPL_ADMINEMAIL
        """

        self.logger.info(params[1])

    async def irc_263(self, tags, prefix, command, params):
        """
        RPL_TRYAGAIN
        """

        self.logger.info("%s | %s", params[1], params[2])

    async def irc_265(self, tags, prefix, command, params):
        """
        RPL_LOCALUSERS
        """

        if len(params) > 2:
            current, max = params[1], params[2]  # Optional at the moment
        else:
            # TODO: Validation/error handling
            split = params[1].split(" ")
            current, max = int(split[-3][:-1]), int(split[-1])

        self.logger.info(params[-1])

    async def irc_266(self, tags, prefix, command, params):
        """
        RPL_GLOBALUSERS
        """

        if len(params) > 2:
            current, max = params[1], params[2]  # Optional at the moment
        else:
            # TODO: Validation/error handling
            split = params[1].split(" ")
            current, max = int(split[-3][:-1]), int(split[-1])

        self.logger.info(params[-1])

    async def irc_276(self, tags, prefix, command, params):
        """
        RPL_WHOISCERTFP
        """

        nick = params[1]
        fingerprint = params[2].split(" ")[-1]

        self.logger.info(" ".join(params[1:]))

    async def irc_300(self, tags, prefix, command, params):
        """
        RPL_NONE
        """

    async def irc_301(self, tags, prefix, command, params):
        """
        RPL_AWAY
        """

        nick = params[1]
        message = params[2]

        self.logger.info(" ".join(params[1:]))

    async def irc_302(self, tags, prefix, command, params):
        """
        RPL_USERHOST
        """

        # TODO: Parse as follows:
        # ["<nickname> [*] = <+/-> <hostname>", ...]

    # TODO: The rest of the numerics

    # endregion

    # region: Higher-level API functions

    def send_join(self, channel):
        self.write_line("JOIN {}".format(channel))

    # endregion

    pass
