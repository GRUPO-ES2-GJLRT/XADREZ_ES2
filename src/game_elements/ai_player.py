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
        self.chosen_move = None

    def start_turn(self):
        if not self.chess.game.running:
            sys.exit()
        super(AIPlayer, self).start_turn()
        self.chosen_move = None
        threading.Thread(target=self.ai_move).start()

    def select(self, square):
        super(AIPlayer, self).select(square)
        sleep(0.1)

    def do_move(self, chosen_move):
        chess = self.chess
        while chess.state == scenes.chess.PAUSE:
            self.try_to_exit_thread_loop()
            pass
        self.select(chosen_move[0])
        self.play(chosen_move[1])

    def try_to_exit_thread_loop(self):
        if (self.state == END or self.chess.state in scenes.chess.END_GAME
                or not self.chess.game.running):
            sys.exit(0)

    def ai_move(self):
        if (self.state == END or self.chess.state in scenes.chess.END_GAME):
            return

        if self.level == SOOO_EASY:
            moves = list(self.chess.board.possible_moves(self.color))

            while not moves:
                self.try_to_exit_thread_loop()
                moves = list(self.chess.board.possible_moves(self.color))

            self.do_move(random.choice(moves))

        elif self.level == EASY:
            moves = list(
                self.chess.board.possible_killing_moves(self.color) or
                self.chess.board.possible_moves(self.color)
            )

            while not moves:
                self.try_to_exit_thread_loop()
                moves = list(
                    self.chess.board.possible_killing_moves(self.color) or
                    self.chess.board.possible_moves(self.color)
                )

            self.do_move(random.choice(moves))

        elif self.level == MEDIUM:
            raise Exception

        elif self.level == HARD:
            raise Exception

        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception

    def confirm_draw(self):
        self.chess.deny_draw(self)

    def minmax_alpha_beta_pruning(self, node, depth, a, b, maximizing_player):
        if depth == 0 or node.is_terminal():
            return self.evaluate_state(node)

        if maximizing_player:
            for child in node.childs():
                a = max(a, self.minmax_alpha_beta_prunning(child, depth - 1, a, b, False))
                if b <= a:
                    break
            return a
        else:
            for child in node.childs():
                b = min(b, self.minmax_alpha_beta_prunning(child, depth - 1, a, b, True))
                if b <= a:
                    break
            return a

    @staticmethod
    def evaluate_state(node):
        return node

