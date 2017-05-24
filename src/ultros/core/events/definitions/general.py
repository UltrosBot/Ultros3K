# coding=utf-8

"""
General event types and base classes
"""
from ultros.core.events.definitions.meta import EventMeta

__author__ = "Gareth Coles"


class Event(metaclass=EventMeta):
    """
    An event. Represents something that happened.

    This object should always have a `caller` attribute, to refer to the
    object that created it.

    Additionally, every event should have a unique `identifier` - an attribute
    that uniquely identifies this type of event. It should be a relatively
    short, human-readable string. If left out, one will be generated from the
    class' module and name.

    The `identifiers` attribute is a list that is populated automatically,
    with identifiers representing the subclasses of the event, as well as
    the event's unique identifier. This is used in the event manager for
    handlers that wish to subscribe to large swathes of events.
    """

    # Note: These are set in the metaclass, but exist here to placate static
    # analysis. Check EventMeta's docs for more info.
    identifier = None  # Identifier that applies to this event specifically
    identifiers = None  # Set of identifiers that apply to this event

    cancelled = False  # Whether the event has been cancelled


class PluginEvent(Event):
    """
    An event that's been fired from a plugin.

    Any plugins that fire events should subclass from this.
    """

    def __init__(self, plugin):  # TODO: Typing
        super().__init__()

        self.plugin = plugin


class ProtocolEvent(Event):
    """
    An event that's been fired from a protocol.

    Any protocols that fire events should subclass from this.
    """

    def __init__(self, protocol):  # TODO: Typing
        super().__init__()

        self.protocol = protocol
