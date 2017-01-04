# coding=utf-8

"""
The event manager
"""

from asyncio.coroutines import iscoroutinefunction, _CoroutineABC

from operator import itemgetter
from typing import Callable, Union, Optional

from ultros.events.constants import EventPriority
from ultros.events.definitions.general import Event

__author__ = "Gareth Coles"


class EventManager:
    """
    The event manager is in charge of firing events and calling handlers.

    Our event system is very flexible, but requires correct usage in order
    to function properly. Read over these docs, and if you get stuck, take
    a look at the unit tests or send us a message on IRC.
    """

    registered = None
    # {
    #     "identifier": [
    #         {
    #             "owner": "",
    #             "callable": "",
    #             "priority": "",
    #             "filter": "",
    #             "cancelled": "",
    #             "args": [],
    #             "kwargs": {}
    #         },
    #     ]
    # }

    def __init__(self):
        self.registered = {}

    def _get_identifier(self, identifier: Union[str, Event]):
        if isinstance(identifier, str):
            return identifier
        try:
            return identifier.identifier
        except AttributeError:
            raise TypeError("identifier must be of type str or Event")

    def add_handler(self,
                    # Required args
                    owner: object,
                    identifier: Union[str, Event],
                    func: Callable[..., Optional[_CoroutineABC]],

                    # Optional args
                    priority: Union[EventPriority, int] = EventPriority.NORMAL,
                    filter_func: Callable[[Event], bool] = None,
                    cancelled: bool = False,
                    args: list = None,
                    kwargs: dict = None):
        """
        Register a handler to listen for events.

        Event handlers are callables (functions or classes with
        :code:`__call__()` defined) that are called in response to an event
        being fired. This allows your code to react to things happening in
        real-time.

        * Please remember to pass in the correct :code:`owner` parameter. If
          you're writing a plugin, this should be the instance of your plugin,
          so that the handlers can be cleaned up automatically when it is
          unloaded.
        * Identifiers may be event classes or strings. They allow you to match
          large numbers of different events in the same handler. Each event is
          equipped with its own identifier, and a list of identifiers that
          belong to its superclasses. You may either pass in one of these
          identifiers (if you happen to know it) or, preferably, pass in one of
          the superclasses you'd like to match. For example, if you wanted to
          match every event fired by a plugin, you might pass in
          :code:`ultros.events.general.PluginEvent` here.

          * Passing in these classes is preferred as identifiers may change.
            If you pass in a class, the event manager will figure out the
            correct identifier to use for you.

        * Event priorities serve as a way to decide which handlers get called
          first. If you don't care, you can omit one, but you can pass one in
          if requred.

          * Event priorities are ordered from lowest to highest, using Python's
            standard sorting algorithm. You may pass in an
            :code:`EventPriority` from :code:`ultros.events.constants`, or
            provide an integer instead if that isn't fine-grained enough for
            you.

        :param owner: The object that owns this handler. Used for cleanup.
        :param identifier: An identifier or base event class to match against.
                           See above for more.
        :param func: Your handler callable. This will be called when a matching
                     event is fired. It may be a standard callable, or a
                     coroutine as needed.

        :param priority: Dictates when your handler is called in relation to
                         other registered handlers that match the same event.
                         See above for more info on that.
        :param filter_func: A function called before your handler with a
                            matched event and returning a boolean. This allows
                            more fine-grained matching - return False to
                            prevent your handler from being called, True to
                            allow it to be called.
        :param cancelled: Whether to allow cancelled events to be matched.
        :param args: Extra arguments that will be passed to your handler when
                     called.
        :param kwargs: Extra keyword arguments that will be passed to your
                       handler when called.
        """

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        identifier = self._get_identifier(identifier)

        if identifier not in self.registered:
            self.registered[identifier] = []

        handler = {
            "owner": owner,
            "callable": func,
            "priority": priority,
            "filter": filter_func,
            "cancelled": cancelled,
            "args": args,
            "kwargs": kwargs
        }

        self.registered[identifier].append(handler)
        self.registered[identifier].sort(key=itemgetter("priority"))

    def remove_handler(self,
                       func: Callable[..., Optional[_CoroutineABC]],
                       identifier: Union[str, Event] = None,
                       priority: EventPriority = None):
        """
        Remove a registered handler given specific matching criteria.

        We provide extra criteria here because handler functions may be
        registered multiple times.

        :param func: The handler function to look for
        :param identifier: An identifier or base event class to match against.
        :param priority: The event priority the handler was registered with.
        """

        if identifier is None:
            handler_dict = self.registered
        else:
            identifier = self._get_identifier(identifier)
            handler_dict = {None: self.registered.get(identifier, {})}

        for ident, handlers in handler_dict.items():
            for x in range(len(handlers) - 1, -1, -1):
                handler = handlers[x]
                if handler["callable"] == func:
                    if priority is None or priority == handler["priority"]:
                        handlers.pop(x)

    def remove_handlers_for_owner(self, owner: object):
        """
        Remove all handlers owned by a specific object. Mostly used for
        cleanup.

        :param owner: The owning object to match against.
        """

        for ident, handlers in self.registered.items():
            for x in range(len(handlers) - 1, -1, -1):
                handler = handlers[x]
                if handler["owner"] == owner:
                    handlers.pop(x)

    async def fire_event(self, event: Event) -> Event:
        """
        Fire an event, and call the handlers registered for it. This is a
        coroutine, and so needs to be awaited.

        Note that handlers are (by design) allowed to modify events. The
        event you passed in is returned in case you need to do any advanced
        coroutine processing.

        :param event: The event object to be fired.
        :return: The event object you passed in.
        """

        for identifier in event.identifiers:
            handlers = self.registered.get(identifier, [])
            for handler in handlers:
                if event.cancelled and not handler["cancelled"]:
                    continue
                if handler["filter"] and not handler["filter"](event):
                    continue

                func = handler["callable"]
                args = handler["args"]
                kwargs = handler["kwargs"]

                try:
                    if iscoroutinefunction(func):
                        await func(event, *args, **kwargs)
                    else:
                        func(event, *args, **kwargs)
                except Exception:
                    # TODO: Logging
                    raise
        return event
