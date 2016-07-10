# coding=utf-8
from asyncio.coroutines import iscoroutinefunction

from operator import itemgetter

from types import FunctionType

from ultros.events.constants import EventPriority
from ultros.events.definitions.general import Event

__author__ = 'Gareth Coles'


class EventManager:
    registered = {
        # "identifier": [
        #     {
        #         "owner": "",
        #         "callable": "",
        #         "priority": "",
        #         "filter": "",
        #         "cancelled": "",
        #         "args": [],
        #         "kwargs": {}
        #     },
        # ]
    }

    def add_callback(self,
                     # Required args
                     owner: object,
                     identifier: str,
                     func: FunctionType,
                     priority: EventPriority,

                     # Optional args
                     filter_func: FunctionType,
                     cancelled: bool = False,
                     args: list = None,
                     kwargs: dict = None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

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

    async def run_callback(self, event: Event) -> Event:
        if event.identifier in self.registered:
            handlers = sorted(
                self.registered[event.identifier], key=itemgetter("priority")
            )

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
                except Exception as e:
                    # TODO: Logging
                    pass
        return event
