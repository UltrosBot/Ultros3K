Module layout
=============

Previous versions of Ultros had a structure similar to the following:

* :code:`/` (Application root)

  * :code:`plugins/`

    * :code:`<plugin_name>/`

      * :code:`__init__.py`

  * :code:`system/`

    * :code:`events/`
    * :code:`plugins/`
    * :code:`protocols/`
    * :code:`storage/`

While this worked okay, the code was designed around everything being contained
within a single base folder. This makes it very difficult to convert to an
installable form (for example, using :code:`setup.py`).

As we're now creating a proper installable module, we've changed the layout, as
follows.

* :code:`/src` (Source root)

  * :code:`ultros/`

    * :code:`events/`
    * :code:`networks/`
    * :code:`plugins/`
    * :code:`rules/`
    * :code:`storage/`
    * :code:`__init__.py`
    * :code:`__main__.py` (Main application runner)


