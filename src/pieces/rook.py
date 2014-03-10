# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import LinearExplorationPiece

class Rook(LinearExplorationPiece):

    def name(self):
        return "rook"

    def possible_moves(self, hindered=True):
        result = {}
        # Bottom
        for y in xrange(self.y + 1, 8):
            position = (self.x, y)
            if not self.explore_position_and_continue(position, result):
                break
        # Top
        for y in xrange(self.y - 1, -1, -1):
            position = (self.x, y)
            if not self.explore_position_and_continue(position, result):
                break
        # Left
        for x in xrange(self.x + 1, 8):
            position = (x, self.y)
            if not self.explore_position_and_continue(position, result):
                break
        # Right
        for x in xrange(self.x - 1, -1, -1):
            position = (x, self.y)
            if not self.explore_position_and_continue(position, result):
                break

        return result

