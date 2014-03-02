# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import LinearExplorationPiece

class Tower(LinearExplorationPiece):

    def possible_moves(self):
        result = set()

        for y in xrange(self.y + 1, 8):
            position = (self.x, y)
            if not self.explore_position_and_continue(position, result):
                break
        for y in xrange(self.y - 1, -1, -1):
            position = (self.x, y)
            if not self.explore_position_and_continue(position, result):
                break
        for x in xrange(self.x + 1, 8):
            position = (x, self.y)
            if not self.explore_position_and_continue(position, result):
                break
        for x in xrange(self.x - 1, -1, -1):
            position = (x, self.y)
            if not self.explore_position_and_continue(position, result):
                break

        return result

