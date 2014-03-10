# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import Piece

class Knight(Piece):

    def name(self):
        return "knight"

    def possible_moves(self, hindered=True):
        moves = [
            (self.x - 2, self.y - 1), (self.x - 2, self.y + 1),
            (self.x - 1, self.y - 2), (self.x - 1, self.y + 2),
            (self.x + 2, self.y - 1), (self.x + 2, self.y + 1),
            (self.x + 1, self.y - 2), (self.x + 1, self.y + 2),
        ]
        
        return set(position for position in moves if self.valid_move(position))

    