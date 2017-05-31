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
        self.ultros = ultros
        self.log = logging.getLogger("Networks")

    def shutdown(self):
        self.ultros = None

    def _load_network(self, name) -> Optional[BaseNetwork]:
        self.log.info("Loading network: {}", name)

        config = self.ultros.storage_manager.get_config(
            "networks/{}.yml".format(name)
        )

        network_cls = self._get_class(config["type"])

        if not network_cls:
            return None

        return network_cls(name, config)

    def _get_class(self, module_name) -> Optional[type(BaseNetwork)]:
        module = importlib.import_module(PACKAGE.format(module_name))

        for name, network_cls in inspect.getmembers(module):
            if inspect.isclass(network_cls):
                if network_cls != BaseNetwork:
                    for parent in inspect.getmro(network_cls):
                        if parent == BaseNetwork:
                            return network_cls
