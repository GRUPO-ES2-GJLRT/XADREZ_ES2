# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .bishop import Bishop
from .rook import Rook

class Queen(Bishop, Rook):

    def name(self):
        return "queen"

    def possible_moves(self, hindered=True, hindered_positions=None):
        return dict(Bishop.possible_moves(self), **Rook.possible_moves(self))
