# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .linear_exploration_piece import LinearExplorationPiece


class Bishop(LinearExplorationPiece):

    def name(self):
        return "bishop"

    def possible_moves(self):
        move = {}
        enemy = {}
        ally = {}
        _, allowed = self.get_allowed()
        # Top Left
        for i in xrange(1, min(self.x, self.y) + 1):
            position = (self.x - i, self.y - i)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Top Right
        for i in xrange(1, min(8 - self.x, self.y) + 1):
            position = (self.x + i, self.y - i)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Bottom Left
        for i in xrange(1, min(self.x, 8 - self.y) + 1):
            position = (self.x - i, self.y + i)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break
        # Bottom Right
        for i in xrange(1, min(8 - self.x, 8 - self.y) + 1):
            position = (self.x + i, self.y + i)
            if not self.explore_position(position, move, enemy, ally, allowed):
                break

        return move, enemy
