# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
import threading
from time import sleep
from .player import Player

SOOO_EASY = 0
EASY = 1
MEDIUM = 2
HARD = 3
SUCH_HARD_MUCH_DIFFICULT = 4


class AIPlayer(Player):

    def __init__(self, color, timer, chess, level, *args, **kwargs):
        super(AIPlayer, self).__init__(color, timer, chess, *args, **kwargs)
        self.level = level
        self.board = chess.board

    def start_turn(self):
        if not self.chess.game.running:
            sys.exit()
        super(AIPlayer, self).start_turn()
        threading.Thread(target=self.ai_move).start()

    def select(self, square):
        super(AIPlayer, self).select(square)
        sleep(1)

    def ai_move(self):
        if not self.chess.state is None:
            return

        if self.level == SOOO_EASY:
            move = random.choice(list(
                self.chess.board.possible_moves(self.color)
            ))
            self.select(move[0])
            self.play(move[1])

        elif self.level == EASY:
            move = random.choice(list(
                self.chess.board.possible_killing_moves(self.color) or
                self.chess.board.possible_moves(self.color)
            ))
            self.select(move[0])
            self.play(move[1])

        elif self.level == MEDIUM:
            raise Exception

        elif self.level == HARD:
            raise Exception

        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception
