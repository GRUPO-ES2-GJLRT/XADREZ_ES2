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
        Player.start_turn(self)
        threading.Thread(target=self.ai_move).start()

    def ai_move(self):
        if not self.chess.state is None:
            return

        if self.level == SOOO_EASY:
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
        elif self.level == EASY:
            move_to_make = None
            moved = False
            while not moved:
                possible_moves = self.chess.board.possible_moves(self.color)
                if not len(possible_moves) == 0:
                    moves = list(possible_moves)
                    for move in moves:
                        if self.board.has_piece(move[1], self.chess.other_player.color):
                            move_to_make = move
                            break

                    if move_to_make is None:
                        move_to_make = random.choice(list(possible_moves))

                    self.select(move_to_make[0])
                    sleep(1)
                    moved = self.play(move_to_make[1])
                else:
                    moved = True
        elif self.level == MEDIUM:
            raise Exception
        elif self.level == HARD:
            raise Exception
        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception
