# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .bishop import Bishop
from .rook import Rook


class Queen(Bishop, Rook):

    def name(self):
        return "queen"

    def possible_moves(self, hindered=True, hindered_positions=None):
        bishop = Bishop.possible_moves(self)
        bishop = bishop[0].copy(), bishop[1].copy()
        rook = Rook.possible_moves(self)
        bishop[0].update(rook[0])
        bishop[1].update(rook[1])
        return bishop
