# coding=utf-8

"""
General event types and base classes

Members
=======
"""

__author__ = 'Gareth Coles'


class Event:
    """
    An event. Represents something that happened.

    This object should always have a `caller` attribute, to refer to the
    object that created it.

    Additionally, every event should have a unique `identifier` - an attribute
    that uniquely identifies this type of event. It should be a relatively
    short, human-readable string.

    The `identifiers` attribute is a list that is populated automatically,
    with identifiers representing the subclasses of the event, as well as
    the event's unique identifier. This is used in the event manager for
    handlers that wish to subscribe to large swathes of events.
    """

    identifier = "Event"  # Unique event type identifier
    identifiers = None  # Set of identifiers that apply to this event

    cancelled = False  # Whether the event has been cancelled

    def __init__(self):
        self.identifiers = {"Event"}
        self.identifiers.add(self.identifier)


class PluginEvent(Event):
    """
    An event that's been fired from a plugin.

    Any plugins that fire events should subclass from this.
    """

    identifier = "PluginEvent"

    def __init__(self, plugin):  # TODO: Typing
        super().__init__()

        self.plugin = plugin
        self.identifiers.add("PluginEvent")


class ProtocolEvent(Event):
    """
    An event that's been fired from a protocol.

    Any protocols that fire events should subclass from this.
    """

    identifier = "ProtocolEvent"

    def __init__(self, protocol):  # TODO: Typing
        super().__init__()

        self.protocol = protocol
        self.identifiers.add("ProtocolEvent")
