# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
import threading
from time import sleep
from .player import Player, END
import scenes

PLAYER = None
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
        self.playing = False

    def start_turn(self):
        if not self.chess.game.running:
            sys.exit()
        super(AIPlayer, self).start_turn()
        self.playing = False
        threading.Thread(target=self.ai_move).start()

    def resume_turn(self):
        super(AIPlayer, self).resume_turn()
        if not self.playing:
            threading.Thread(target=self.ai_move).start()

    def select(self, square):
        super(AIPlayer, self).select(square)
        sleep(0.1)

    def ai_move(self):
        if not self.chess.state is None and not self.state == END:
            return
        self.playing = False
        if self.chess.state == scenes.chess.PAUSE:
            return
        self.playing = True

        if self.level == SOOO_EASY:
            moves = list(self.chess.board.possible_moves(self.color))

            while not moves:
                moves = list(self.chess.board.possible_moves(self.color))

            move = random.choice(moves)
            self.select(move[0])
            self.play(move[1])

        elif self.level == EASY:
            moves = list(
                self.chess.board.possible_killing_moves(self.color) or
                self.chess.board.possible_moves(self.color)
            )

            while not moves:
                moves = list(
                    self.chess.board.possible_killing_moves(self.color) or
                    self.chess.board.possible_moves(self.color)
                )

            move = random.choice(moves)
            if self.chess.state == scenes.chess.PAUSE:
                return
            self.select(move[0])
            self.play(move[1])

        elif self.level == MEDIUM:
            raise Exception

        elif self.level == HARD:
            raise Exception

        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception

    def confirm_draw(self):
        self.chess.deny_draw(self)
