# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import Piece

class King(Piece):

    def name(self):
        return "king"

    def possible_moves(self):
        moves = [
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 1), 
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 1),
            (self.x, self.y - 1), (self.x, self.y + 1),
            (self.x - 1, self.y), (self.x + 1, self.y),
        ]
        
        return set(position for position in moves if self.valid_move(position))

    