Connectors
==========

.. note::

    This document is very much a work in progress and may change frequently
    up until a stable release.

.. warning::

    Everything below this spot is provisional. YMMV!

A Connector is a low-level implementation of a chat network protocol. It
handles all of the basic networking for that protocol, providing medium-level
functions and packet notification for :doc:`servers`.

As some chat networks require multiple connections - often with differing
protocols - the number of connectors tracked by a :doc:`Network <networks>`
may be different to the number of :doc:`servers` it tracks. Indeed, there
may even be multiple types of connectors under a single
:doc:`Network <networks>`.

Connectors provide basic network functionality, and are the backbone to any
:doc:`Server <servers>`.
