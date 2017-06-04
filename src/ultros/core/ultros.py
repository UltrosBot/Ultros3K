# coding=utf-8
import asyncio
import logging
import signal

import sys
from typing import Optional

from ultros.core.events import manager as event_manager
from ultros.core.networks import manager as network_manager
from ultros.core.plugins import manager as plugin_manager
from ultros.core.storage import manager as storage_manager

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
    """
    The Ultros class. Home for all system-wide components.

    :param config_dir: Directory containing configuration files
    :param data_dir: Directory to contain data files
    :param event_loop: Optionally, the event loop to work with. Omit this and the instance will create one itself,
                       preferring `uvloop` if installed. If you don't want to use uvloop, pass in a loop yourself.
    :param handle_signals: If you don't want SIGTERM, SIGINT and SIGBREAK handled automatically (eg, you have more
                           than one Ultros instance), then set this to False.
    """

    event_manager = None
    network_manager = None
    plugin_manager = None
    storage_manager = None

    def __init__(self, config_dir: str, data_dir: str, event_loop: Optional[asyncio.BaseEventLoop]=None,
                 handle_signals: bool=True):
        self.do_stop = False

        # TODO: Proper logging
        self.log = logging.getLogger(__name__)

        if not event_loop:
            try:
                import uvloop
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                self.log.debug("Found uvloop; using for default event loop policy")
            except Exception as e:
                self.log.debug("Unable to import uvloop; using default asyncio event loop policy: %s", e)

            event_loop = asyncio.get_event_loop()

        self.event_loop = event_loop

        self.log.info("Starting up...")

        # Load order is important
        self.storage_manager = storage_manager.StorageManager(
            self, config_dir, data_dir
        )

        self.event_manager = event_manager.EventManager(self)
        self.plugin_manager = plugin_manager.PluginManager(self)
        self.network_manager = network_manager.NetworkManager(self)

        if handle_signals:
            signal.signal(signal.SIGINT, self._sigint)
            signal.signal(signal.SIGTERM, self._sigterm)

            if hasattr(signal, "SIGBREAK"):  # Windows only
                signal.signal(signal.SIGBREAK, self._sigbreak)

    def _sigterm(self, *_):
        """
        Handle SIGTERM and shut down gracefully.
        """

        self.log.debug("SIGTERM caught.")
        asyncio.run_coroutine_threadsafe(self.shutdown(), self.event_loop)

    def _sigint(self, *_):
        """
        Handle CTRL+C or SIGINT and shut down gracefully.
        """

        print("")  # Or it'll print on the same line as the ^C
        self.log.debug("SIGINT caught.")
        asyncio.run_coroutine_threadsafe(self.shutdown(), self.event_loop)

    def _sigbreak(self, *_):
        """
        Handle SIGBREAK (CTRL+BREAK or closing the CMD window) on Windows and shut down gracefully.

        Note that we only get five seconds when this happens before the process is killed, so we should try
        to keep this process fast.
        """

        self.log.debug("SIGBREAK caught.")
        asyncio.run_coroutine_threadsafe(self.shutdown(), self.event_loop)

    async def shutdown(self):
        """
        Gracefully shut down this Ultros instance.

        In order, this unloads the network manager, plugin manager, event manager and storage manager,
        and then stops the event loop if instructed to earlier (eg by calling `.run()`).
        """

        self.log.info("Shutting down...")

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

        if self.event_manager:
            try:
                self.event_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.event_manager = None

        if self.storage_manager:
            try:
                self.storage_manager.shutdown()
            except Exception as e:
                print(e)  # TODO: Logging

            self.storage_manager = None

        if self.do_stop:
            self.event_loop.stop()
            self.event_loop.close()

    def setup(self):
        """
        Set up this Ultros instance.

        This will parse configs, load plugins, and get networks connected. The managers however have already been
        instantiated.
        """

        self.network_manager.load_networks()
        asyncio.run_coroutine_threadsafe(self.network_manager.connect_all(), self.event_loop)

    def run(self):
        """
        Convenience function for running a single instance.

        This will instruct the current instance to stop its event loop on shutdown, and will make that loop
        run forever, blocking this thread with it.

        If you don't want this, you can handle the event loop management yourself instead.
        """

        self.do_stop = True
        self.event_loop.run_forever()
