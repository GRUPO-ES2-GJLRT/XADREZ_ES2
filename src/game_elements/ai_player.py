# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random

from .player import Player

EASY = 0
MEDIUM = 1
HARD = 2
SUCH_HARD_MUCH_DIFFICULT = 3


class AIPlayer(Player):

    def __init__(self, color, timer, chess, level, *args, **kwargs):
        super(AIPlayer, self).__init__(color, timer, chess, *args, **kwargs)
        self.level = level
        self.board = chess.board

    def start_turn(self):
        Player.start_turn(self)
        #import threading
        #threading.Timer(1, self.ai_move).start()
        self.ai_move()

    def ai_move(self):
        if self.level == 0:
            moved = False
            while not moved:
                possible_moves = self.chess.board.possible_moves(self.color)
                if not len(possible_moves) == 0:
                    move = random.choice(list(possible_moves))
                    self.select(move[0])
                    moved = self.play(move[1])
                else:
                    moved = True
