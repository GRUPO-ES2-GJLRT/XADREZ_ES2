# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random

from consts.colors import BLACK
from .player import Player

EASY = 0
MEDIUM = 1
HARD = 2
SUCH_HARD_MUCH_DIFFICULT = 3


class AIPlayer(Player):

    def __init__(self, color, timer, level,  board, *args, **kwargs):
        super(AIPlayer, self).__init__(color, timer, *args, **kwargs)
        self.level = level
        self.board = board

    def play(self):
        if self.level == 0:
            possible_moves = self.board.possible_moves(BLACK)
            if not len(possible_moves) == 0:
                move = possible_moves.keys()[
                    random.randint(0, len(possible_moves.keys()) - 1)
                ]
                return self.board.move(move[0], move[1])

            return None
