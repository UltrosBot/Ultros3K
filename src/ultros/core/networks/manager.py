# coding=utf-8
import importlib
import inspect
import logging

from typing import Optional

from ultros.core import ultros as u
from ultros.core.networks.base.networks.base import BaseNetwork

__author__ = "Gareth Coles"
PACKAGE = "ultros.networks.{}.network"


class NetworkManager:
    def __init__(self, ultros: "u.Ultros"):
        self.log = logging.getLogger("Networks")  # TODO: Proper logging
        self.ultros = ultros

        self.networks = {}

    def shutdown(self):
        self.ultros = None

    def load_networks(self):
        config = self.ultros.storage_manager.get_config("settings.yml", defaults_path=False)
        network_list = config["networks"]

        if not network_list:
            self.log.warning("No networks have been configured!")

        for network_name in network_list:
            network = self._load_network(network_name)

            if not network:
                self.log.error("Unknown network type for %s", network_name)
                continue

            self.networks[network_name] = network

    async def connect_all(self):
        for network_name, network in self.networks.items():
            self.log.info("Setting up: %s", network_name)
            await network.setup()

    def _load_network(self, name) -> Optional[BaseNetwork]:
        self.log.info("Loading network: %s", name)

        config = self.ultros.storage_manager.get_config(
            "networks/{}.yml".format(name)
        )

        network_cls = self._get_class(config["type"])

        if not network_cls:
            return None

        return network_cls(name, config, self.ultros)

    def _get_class(self, module_name) -> Optional[type(BaseNetwork)]:
        module = importlib.import_module(PACKAGE.format(module_name))

        for name, network_cls in inspect.getmembers(module):
            if inspect.isclass(network_cls):
                if network_cls != BaseNetwork:
                    for parent in inspect.getmro(network_cls):
                        if parent == BaseNetwork:
                            return network_cls
