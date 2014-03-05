# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import LinearExplorationPiece

class Bishop(LinearExplorationPiece):

    def name(self):
        return "bishop"

    def possible_moves(self):
        result = set()
        # Top Left
        for i in xrange(1, min(self.x, self.y) + 1):
            position = (self.x - i, self.y - i)
            if not self.explore_position_and_continue(position, result):
                break
        # Top Right
        for i in xrange(1, min(8 - self.x, self.y) + 1):
            position = (self.x + i, self.y - i)
            if not self.explore_position_and_continue(position, result):
                break
        # Bottom Left
        for i in xrange(1, min(self.x, 8 - self.y) + 1):
            position = (self.x - i, self.y + i)
            if not self.explore_position_and_continue(position, result):
                break
        # Bottom Right
        for i in xrange(1, min(8 - self.x, 8 - self.y) + 1):
            position = (self.x + i, self.y + i)
            if not self.explore_position_and_continue(position, result):
                break

        return result
