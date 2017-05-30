IRC
===

.. note::

    This document is very much a work in progress and may change frequently
    up until a stable release.


.. warning::

    Everything below this spot is provisional. YMMV!

With IRC, the process might look something like this:


Network
-------

* The Network reads in the configuration for this IRC net
* A Server named after the IRC connection hostname is created
* A TCP/SSL Connector is created for the IRC connection and associated with the server

Connector
---------

* The connector does the handshake and notifies the server that it has connected
* The connector parses all of the incoming data
    * If anything needs to be handled automatically (eg, PING), then that happens in the connector
    * All incoming data is also passed to the server for further processing

Server
------

* The server uses the connector to join configured channels and run the perform
* The server fires any required events and handles all API calls, using the connector to send data as needed

Disconnection
-------------

* If the connection drops for some reason, the network is notified
    * The network destroys the server and the connector
    * If reconnection is configured, the network creates a new server and connector and starts again
    * If reconnection is not configured, the network requests its own removal from the network manager

* If disconnection is requested by the network
    * The network requests that the server disconnects
    * The server handles a graceful disconnection
    * The network cleans itself up and requests its own removal from the network manager

* If disconnection is requested by the server
    * The server handles a graceful disconnection
    * The server requests its own removal from the network
    * The network cleans itself up and requests its own removal from the network manager
