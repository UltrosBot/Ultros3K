# coding=utf-8
import asyncio
import inspect
from functools import partial

from ultros.core.events.constants import EventPriority
from ultros.core.events.definitions.general import Event, PluginEvent, NetworkEvent
from ultros.core.events.definitions.meta import EventMeta
from ultros.core.events.manager import EventManager

from nose.tools import assert_equal, assert_true, assert_false, assert_raises
from unittest import TestCase


__author__ = "Sean"


class TestEvents(TestCase):
    def setUp(self):
        self.manager = EventManager(None)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        del self.manager
        del self.loop

    def test_basic(self):
        """
        Events system basics
        """
        fired = False
        other_fired = False

        def handler(event):
            nonlocal fired
            fired = True

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        self.manager.add_handler(self, Event, handler)
        self.manager.add_handler(self, "different event", other_handler)

        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_true(fired, "Event handler didn't fire")
        assert_false(other_fired, "Other event handler should not have fired")

    def test_get_identifier(self):
        """
        Identifier retrieval by manager
        """
        assert_equal(
            self.manager._get_identifier("Test"),
            "Test"
        )
        assert_equal(self.manager._get_identifier(
            Event()),
            "ultros.core.events.definitions.general.Event"
        )

        assert_raises(TypeError, self.manager._get_identifier, 12)
        assert_raises(TypeError, self.manager._get_identifier, None)

    def test_async(self):
        """
        Events system async handler
        """
        fired = False

        async def handler(event):
            nonlocal fired
            fired = True

        async def other_handler(event):
            raise NotImplementedError("This should be raised!")

        self.manager.add_handler(self, Event, handler)
        self.loop.run_until_complete(self.manager.fire_event(Event()))
        self.manager.remove_handlers_for_owner(self)

        assert_true(fired, "Event handler didn't fire")

        self.manager.add_handler(self, Event, other_handler)

        assert_raises(
            NotImplementedError,
            self.loop.run_until_complete,
            self.manager.fire_event(Event())
        )

    def test_priority(self):
        """
        Events system priorities
        """
        fired = []

        def handler(event, order):
            fired.append(order)

        handler_1 = partial(handler, order=1)
        handler_2 = partial(handler, order=2)
        handler_3 = partial(handler, order=3)
        handler_4 = partial(handler, order=4)
        handler_5 = partial(handler, order=5)

        self.manager.add_handler(self, Event, handler_1, EventPriority.LOWEST)
        self.manager.add_handler(self, Event, handler_2, EventPriority.LOW)
        self.manager.add_handler(self, Event, handler_3, EventPriority.NORMAL)
        self.manager.add_handler(self, Event, handler_4, EventPriority.HIGH)
        self.manager.add_handler(self, Event, handler_5, EventPriority.HIGHEST)

        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_equal(
            fired,
            [1, 2, 3, 4, 5],
            "Event handlers fired in wrong order"
        )

    def test_cancelled(self):
        """
        Cancelled event handling
        """
        fired = False
        other_fired = False

        def handler(event):
            nonlocal fired
            fired = True

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        self.manager.add_handler(self, Event, handler, cancelled=True)
        self.manager.add_handler(self, Event, other_handler)

        event = Event()
        event.cancelled = True
        self.loop.run_until_complete(self.manager.fire_event(event))

        assert_true(fired, "Event handler didn't fire")
        assert_false(other_fired, "Other event handler should not have fired")

    def test_filter(self):
        """
        Event filtering
        """
        fired = False
        other_fired = False

        def handler(event):
            nonlocal fired
            fired = True

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        def true(event):
            return True

        def false(event):
            return False

        self.manager.add_handler(self, Event, handler)
        self.manager.add_handler(self, Event, handler, filter_func=true)
        self.manager.add_handler(self, Event, other_handler, filter_func=false)

        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_true(fired, "Event handler didn't fire")
        assert_false(other_fired, "Other event handler should not have fired")

    def test_args_kwargs(self):
        """
        Handler args/kwargs
        """
        FOO = "abcde"
        BAR = "fghij"
        fired = None

        def handler(event, foo, *, bar):
            nonlocal fired
            fired = [foo, bar]

        self.manager.add_handler(
            self,
            Event,
            handler,
            args=[FOO],
            kwargs={"bar": BAR},
        )

        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_equal(
            fired,
            [FOO, BAR],
            "Event handler got incorrect args/kwargs"
        )

    def test_remove(self):
        """
        Handler removal
        """
        fired = False

        def handler(event):
            nonlocal fired
            fired = True

        self.manager.add_handler(self, Event, handler)
        self.manager.remove_handler(handler)
        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_false(fired, "Removed handler fired")

    def test_remove_specific(self):
        """
        Specific handler removal
        """
        fired = False
        other_fired = False

        def handler(event):
            nonlocal fired
            fired = True

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        self.manager.add_handler(self, Event, handler, EventPriority.NORMAL)
        self.manager.add_handler(self, Event, other_handler, EventPriority.LOW)
        self.manager.remove_handler(handler, Event, EventPriority.NORMAL)
        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_false(fired, "Removed handler fired")
        assert_true(other_fired, "Other handler shouldn't have been removed")

    def test_remove_owner(self):
        """
        Removing handlers for owner
        """
        fired = False
        other_fired = False

        def handler(event):
            nonlocal fired
            fired = True

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        owner_1 = object()
        owner_2 = object()

        self.manager.add_handler(owner_1, Event, handler)
        self.manager.add_handler(owner_1, Event, handler)
        self.manager.add_handler(owner_1, Event, handler)
        self.manager.add_handler(owner_1, Event, handler)
        self.manager.add_handler(owner_2, Event, other_handler)
        self.manager.add_handler(owner_2, Event, other_handler)
        self.manager.add_handler(owner_2, Event, other_handler)
        self.manager.add_handler(owner_2, Event, other_handler)
        self.manager.remove_handlers_for_owner(owner_1)
        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_false(fired, "Removed handler fired")
        assert_true(other_fired, "Other handler shouldn't have been removed")

    def test_event_identifiers_list(self):
        """
        Event handler firing based on identifiers list
        """
        fired = []
        other_fired = False

        def handler(event, name):
            fired.append(name)

        event_handler = partial(handler, name="Event")
        subevent_handler = partial(handler, name="SubEvent")

        def other_handler(event):
            nonlocal other_fired
            other_fired = True

        class SubEvent(Event):
            pass

        class MoreSubEvent(SubEvent):
            pass

        class DifferentEvent(Event):
            pass

        self.manager.add_handler(self, Event, event_handler)
        self.manager.add_handler(self, SubEvent, subevent_handler)
        self.manager.add_handler(self, MoreSubEvent, other_handler)
        self.manager.add_handler(self, DifferentEvent, other_handler)

        self.loop.run_until_complete(self.manager.fire_event(SubEvent()))

        assert_equal(fired, ["Event", "SubEvent"], "Removed handler fired")
        assert_false(other_fired, "Other handler shouldn't have fired")

    def test_event_metaclass_identifiers(self):
        """
        Event's metaclass identifier[s] creation.
        """
        # These end up with pretty unwieldy and ugly generated names, but only
        # because they're created inside a function inside a class.

        # To avoid this test breaking by accident if the test itself is renamed
        # or moved, don't hard-code its names or location.
        base_identifier = "%s.%s.%s.<locals>" % (self.__class__.__module__,
                                                 self.__class__.__qualname__,
                                                 inspect.stack()[0].function)

        class BaseEvent(metaclass=EventMeta):
            pass

        class FooEvent(BaseEvent):
            identifier = "foo"

        class BarEvent(BaseEvent):
            pass

        class QuxEvent(FooEvent):
            pass

        class PluginBaseEvent(PluginEvent, metaclass=EventMeta):
            pass

        class NetworkBaseEvent(NetworkEvent, metaclass=EventMeta):
            pass

        # Check identifier
        assert_equal(
            Event.identifier,
            "ultros.core.events.definitions.general.Event"
        )
        assert_equal(FooEvent.identifier, "foo")
        assert_equal(
            BarEvent.identifier,
            base_identifier + ".BarEvent"
        )
        assert_equal(
            QuxEvent.identifier,
            base_identifier + ".QuxEvent"
        )

        assert_equal(
            PluginBaseEvent.identifier,
            base_identifier + ".PluginBaseEvent"
        )
        assert_equal(
            NetworkBaseEvent.identifier,
            base_identifier + ".NetworkBaseEvent"
        )

        # Check this matches when init is run also
        assert_equal(
            PluginBaseEvent(None).identifier,
            base_identifier + ".PluginBaseEvent"
        )
        assert_equal(
            NetworkBaseEvent(None).identifier,
            base_identifier + ".NetworkBaseEvent"
        )

        # Check identifiers
        assert_equal(Event.identifiers, [
            "ultros.core.events.definitions.general.Event"
        ])
        assert_equal(FooEvent.identifiers, [
            base_identifier + ".BaseEvent",
            "foo"
        ])
        assert_equal(BarEvent.identifiers, [
            base_identifier + ".BaseEvent",
            base_identifier + ".BarEvent"
        ])
        assert_equal(QuxEvent.identifiers, [
            base_identifier + ".BaseEvent",
            "foo",
            base_identifier + ".QuxEvent"
        ])
