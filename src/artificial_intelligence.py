# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import random

from consts.colors import BLACK

EASY = 0
MEDIUM = 1
HARD = 2
SUCH_HARD_MUCH_DIFFICULT = 3


class ArtificialIntelligence():

    def __init__(self, board, level):
        self.level = level
        self.board = board

    def play(self):
        if self.level == 0:
            possible_moves = self.board.possible_moves(BLACK)
            move = possible_moves.keys()[random.randint(0, len(possible_moves.keys()) - 1)]

            self.board.move(move[0], move[1])
