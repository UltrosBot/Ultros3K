Servers
=======

.. note::

    This document is very much a work in progress and may change frequently
    up until a stable release.

.. warning::

    Everything below this spot is provisional. YMMV!

Servers are an abstract concept that describe, at a high level, one instance
of a client for a specific chat network. They may be associated with one or more
:doc:`connectors`, and provide a level of abstraction that should be relatively
friendly and easy to use for plugin developers and other people working with
Ultros.

Servers contain absolutely no networking code. As such, they must do all of
their networking through :doc:`connectors` - and should request any that they
need from the :doc:`Network <networks>` that manages them, instead of creating
them directly.
