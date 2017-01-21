Networks
========

.. note::

    This document is very much a work in progress and may change frequently
    up until a stable release.

.. warning::

    Everything below this spot is provisional. YMMV!

Networks are in charge of managing :doc:`connectors` and :doc:`servers`. At a
high-level, they exist to manage connections to chat networks of their type,
and provide abstractions for interacting with those networks.

For example, one might decide to write a Network for the IRC protocol. This
Network would then be in charge of creating :doc:`connectors` and
:doc:`servers` for that protocol when requested to by other parts of Ultros.

Networks also manage the lifecycle of both of these, and are expected to
notify the rest of Ultros when servers are created and destroyed.

As some chat networks require multiple connections, some with multiple
protocols, the number of :doc:`connectors` may not match the number of
:doc:`servers`.
