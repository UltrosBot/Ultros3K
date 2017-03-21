# coding=utf-8
from ultros.core import ultros as u

__author__ = "Gareth Coles"


class NetworkManager:
    ultros = None

    def __init__(self, ultros: u.Ultros):
        self.ultros = ultros

    def shutdown(self):
        self.ultros = None
