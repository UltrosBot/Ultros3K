# coding=utf-8
import asyncio
from functools import partial

from ultros.events.constants import EventPriority
from ultros.events.definitions.general import Event
from ultros.events.manager import EventManager

from nose.tools import assert_equal, assert_true, assert_false
from unittest import TestCase


__author__ = "Sean"


class TestEvents(TestCase):
    def setUp(self):
        self.manager = EventManager()

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
        fired = False

        def handler(event):
            nonlocal fired
            fired = True

        self.manager.add_handler(self, Event, handler)
        self.manager.remove_handler(handler)
        self.loop.run_until_complete(self.manager.fire_event(Event()))

        assert_false(fired, "Removed handler fired")

    def test_remove_specific(self):
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
            identifier = "SubEvent"

        class MoreSubEvent(SubEvent):
            identifier = "MoreSubEvent"

        class DifferentEvent(Event):
            identifier = "DifferentEvent"

        self.manager.add_handler(self, Event, event_handler)
        self.manager.add_handler(self, SubEvent, subevent_handler)
        self.manager.add_handler(self, MoreSubEvent, other_handler)
        self.manager.add_handler(self, DifferentEvent, other_handler)

        self.loop.run_until_complete(self.manager.fire_event(SubEvent()))

        assert_equal(fired, ["Event", "SubEvent"], "Removed handler fired")
        assert_false(other_fired, "Other handler shouldn't have fired")
