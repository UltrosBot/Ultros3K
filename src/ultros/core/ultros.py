# coding=utf-8

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


class Ultros:
    event_manager = None
    network_manager = None
    plugin_manager = None
    storage_manager = None

    def __init__(self, config_dir: str, data_dir: str):
        from ultros.core.events import manager as event_manager
        from ultros.core.networks import manager as network_manager
        from ultros.core.plugins import manager as plugin_manager
        from ultros.core.storage import manager as storage_manager

        # Load order is important
        self.storage_manager = storage_manager.StorageManager(self, config_dir, data_dir)
        self.event_manager = event_manager.EventManager(self)
        self.network_manager = network_manager.NetworkManager(self)
        self.plugin_manager = plugin_manager.PluginManager(self)

    def shutdown(self):
        if self.storage_manager:
            try:
                self.storage_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.storage_manager = None

        if self.event_manager:
            try:
                self.event_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.event_manager = None

        if self.network_manager:
            try:
                self.network_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.network_manager = None

        if self.plugin_manager:
            try:
                self.plugin_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.plugin_manager = None
