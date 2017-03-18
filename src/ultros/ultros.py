# coding=utf-8
from ultros.events.manager import EventManager
from ultros.networks.manager import NetworkManager
from ultros.plugins.manager import PluginManager
from ultros.storage.manager import StorageManager

"""
The Ultros class - encapsulation for what matters.

This class could be considered an "instance" of a bot. It contains and manages
instances of the other internal managers - such as the event manager, network
managers, plugin manager and storage manager.

As we've moved away from our previous Singleton-bound implementation, some
way to keep track of everything became necessary. This class will be passed
around all over the place.
"""

__author__ = "Gareth Coles"
__all__ = ["Ultros"]


class Ultros:
    event_manager = None
    network_manager = None
    plugin_manager = None
    storage_manager = None

    def __init__(self, config_dir, data_dir):
        # Load order is important
        self.storage_manager = StorageManager(self, config_dir, data_dir)
        self.event_manager = EventManager(self)
        self.network_manager = NetworkManager(self)
        self.plugin_manager = PluginManager(self)
