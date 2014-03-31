# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
import threading
from time import sleep
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
        if not self.chess.game.running:
            sys.exit()
        Player.start_turn(self)
        threading.Thread(target=self.ai_move).start()

    def ai_move(self):
        if self.level == EASY:
            moved = False
            while not moved:
                possible_moves = self.chess.board.possible_moves(self.color)
                if not len(possible_moves) == 0:
                    move = random.choice(list(possible_moves))
                    self.select(move[0])
                    sleep(1)
                    moved = self.play(move[1])
                else:
                    moved = True
        elif self.level == MEDIUM:
            raise Exception
        elif self.level == HARD:
            raise Exception
        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception
