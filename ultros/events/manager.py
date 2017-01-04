# coding=utf-8
from asyncio.coroutines import iscoroutinefunction, coroutine

from operator import itemgetter
from typing import Callable, Union, Optional

from ultros.events.constants import EventPriority
from ultros.events.definitions.general import Event

__author__ = "Gareth Coles"


class EventManager:
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
                    func: Callable[..., Optional[coroutine]],

                    # Optional args
                    priority: EventPriority = EventPriority.NORMAL,
                    filter_func: Callable[..., bool] = None,
                    cancelled: bool = False,
                    args: list = None,
                    kwargs: dict = None):
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
                       func: Callable[..., None],
                       identifier: Union[str, Event] = None,
                       priority: EventPriority = None):
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
        for ident, handlers in self.registered.items():
            for x in range(len(handlers) - 1, -1, -1):
                handler = handlers[x]
                if handler["owner"] == owner:
                    handlers.pop(x)

    async def fire_event(self, event: Event) -> Event:
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
