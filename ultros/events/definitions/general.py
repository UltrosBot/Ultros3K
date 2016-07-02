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
    identifiers = None  # List of identifiers that apply to this event

    caller = None  # The object responsible for creating the event

    def __init__(self, caller):
        self.caller = caller
        self.identifiers = ["Event"]

        if self.identifier not in self.identifiers:
            self.identifiers.append(self.identifier)


class PluginEvent(Event):
    """
    An event that's been fired from a plugin.

    Any plugins that fire events should subclass from this.
    """

    identifier = "PluginEvent"

    def __init__(self, caller):
        super().__init__(caller)

        self.identifiers.append("PluginEvent")

        if self.identifier not in self.identifiers:
            self.identifiers.append(self.identifier)


class ProtocolEvent(Event):
    """
    An event that's been fired from a protocol.

    Any protocols that fire events should subclass from this.
    """

    identifier = "ProtocolEvent"

    def __init__(self, caller):
        super().__init__(caller)
        self.identifiers.append("ProtocolEvent")

        if self.identifier not in self.identifiers:
            self.identifiers.append(self.identifier)
