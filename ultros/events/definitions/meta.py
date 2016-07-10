# coding=utf-8
__author__ = "Sean"


class EventMeta(type):
    """
    Metaclass for events. Automatically fills in `identifiers` on class
    creation.
    """

    def __new__(metacls, name, bases, class_dict):
        event_cls = super().__new__(metacls, name, bases, class_dict)
        identifiers = []
        event_cls.identifiers = identifiers
        for base in reversed(event_cls.__mro__):
            try:
                identifiers.append(base.identifier)
            except AttributeError:
                pass
        return event_cls
