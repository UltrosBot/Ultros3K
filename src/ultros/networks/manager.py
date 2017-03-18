# coding=utf-8
from ultros import ultros as u
from weakref import ref

__author__ = "Gareth Coles"


class NetworkManager:
    _ultros = None

    @property
    def ultros(self):
        return self.ultros()

    def __init__(self, ultros: u.Ultros):
        self._ultros = ref(ultros)
