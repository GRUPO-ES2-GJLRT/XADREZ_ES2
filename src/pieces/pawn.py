# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import Piece

class Pawn(Piece):

    def possible_moves(self):
        return set()
