# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .linear_exploration_piece import LinearExplorationPiece


class Rook(LinearExplorationPiece):

    @property
    def name(self):
        return "rook"

    def possible_moves(self):
        move = {}
        enemy = {}
        ally = {}
        _, allowed = self.get_allowed()
        # Bottom
        for y in xrange(self.y + 1, 8):
            position = (self.x, y)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Top
        for y in xrange(self.y - 1, -1, -1):
            position = (self.x, y)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Left
        for x in xrange(self.x + 1, 8):
            position = (x, self.y)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Right
        for x in xrange(self.x - 1, -1, -1):
            position = (x, self.y)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break

        return move, enemy
