# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .bishop import Bishop
from .tower import Tower

class Queen(Bishop, Tower):

    def possible_moves(self):
        return Bishop.possible_moves(self).union(Tower.possible_moves(self))
