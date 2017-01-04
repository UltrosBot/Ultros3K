# coding=utf-8

"""
Metaclass for event identifiers

Members
=======
"""

__author__ = "Sean"


class EventMeta(type):
    """
    Metaclass for events. Automatically fills in `identifier` and `identifiers`
    on class creation.

    If class does not have an `identifier` or it is set to None, one is
    generated from its module and class names. This avoids collisions while
    still giving sensible names.
    """

    def __new__(metacls, name, bases, class_dict):
        event_cls = super().__new__(metacls, name, bases, class_dict)
        identifiers = []
        event_cls.identifiers = identifiers
        # Skip event_cls
        for base in reversed(event_cls.__mro__[1:]):
            try:
                identifiers.append(base.identifier)
            except AttributeError:
                # Not an Event
                continue

        # Get or create event_cls identifier
        identifier = class_dict.get("identifier", None)
        if identifier is None:
            identifier = "%s.%s" % (event_cls.__module__,
                                    event_cls.__qualname__)
        event_cls.identifier = identifier
        identifiers.append(identifier)
        return event_cls
