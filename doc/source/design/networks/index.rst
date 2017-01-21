Networks
========

.. note::

    This document is very much a work in progress and may change frequently
    up until a stable release.

Previous versions of Ultros represented chat networks with a relatively
low-level concept: protocols. Protocols were relatively self-contained
implementations of a chat network's networking, along with some higher-level
stuff added (user-level message send functions, event handling, and so on).

While this worked fine for basic setups, it was quite inflexible and we
found that it was difficult to implement certain types of protocols
(particularly those with multiple "servers" per connection). As a result,
we're trying something different.

.. warning::

    Everything below this spot is provisional. YMMV!

This version of Ultros introduces a new concept: Networks. Networks are
collections of Connectors and Servers, and in charge of various duties on
their own. See below for more information on each component.

.. toctree::
    :caption:

    connectors
    networks
    servers
