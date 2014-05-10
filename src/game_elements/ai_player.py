# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
import threading
from collections import Counter
from time import sleep
from consts.moves import (
    CHECKMATE, STALEMATE
)
from consts.pieces import PAWN, KING
from consts.colors import WHITE, BLACK
from .player import Player, END
import scenes
from cython.constants import ILLEGAL, LEGAL, EMPTY
from cython.board import move_key

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
        self.temp_board = self.board
        self.chosen_move = None
        self.openings = {}
        self.skip_validation = True
        self.parse_openings()

    def parse_openings(self):
        with open('../openings.dat') as _file:
            raw_openings = [opening.strip().split() for opening in _file]

        for raw_opening in raw_openings:
            parse_opening(raw_opening, self.openings)

    def start_turn(self):
        if not self.chess.game.running:
            sys.exit()
        super(AIPlayer, self).start_turn()
        self.temp_board = self.board.clone()
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
        if not chosen_move:
            return
        tup = chosen_move.tuple()
        self.select(tup[0])
        self.play(tup[1])
        chess.do_jit_draw()

    def try_to_exit_thread_loop(self):
        if (self.state == END or self.chess.state in scenes.chess.END_GAME
                or not self.chess.game.running):
            sys.exit(0)

    def ai_move(self):
        if (self.state == END or self.chess.state in scenes.chess.END_GAME):
            return

        if self.level == SOOO_EASY:
            moves = list(self.temp_board.possible_moves(self.color))

            while not moves:
                self.try_to_exit_thread_loop()
                moves = list(self.temp_board.possible_moves(self.color))

            self.do_move(random.choice(moves))

        elif self.level == EASY:
            moves = list(
                self.temp_board.possible_killing_moves(self.color) or
                self.temp_board.possible_moves(self.color)
            )

            while not moves:
                self.try_to_exit_thread_loop()
                moves = list(
                    self.temp_board.possible_killing_moves(self.color) or
                    self.temp_board.possible_moves(self.color)
                )

            self.do_move(random.choice(moves))

        elif self.level == MEDIUM:
            self.do_move(self.minmax_move(3))

        elif self.level == HARD:
            self.do_move(self.minmax_move(5))

        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception

    def confirm_draw(self):
        self.chess.deny_draw(self)

    def minmax_move(self, depth):
        a = float('-inf')
        b = float('inf')
        board = self.temp_board
        moves = board.possible_moves(board.color())
        max_move = None
        if moves:
            max_move = moves[0]
        for move in moves:
            move.do_update(board)
            value = -self.negamax_alpha_beta(board, depth - 1, -b, -a,
                1 if board.color() == WHITE else -1)
            move.undo_update(board)
            if value > a:
                max_move = move
                a = value
        return max_move

    def negamax_alpha_beta(self, board, depth, a, b, color):
        moves = board.possible_moves(board.color())
        if depth == 0:
            return color * self.evaluate_state(board)

        best_value = float('-inf')
        for move in moves:
            move.do_update(board)
            value = -self.negamax_alpha_beta(board, depth - 1, -b, -a, -color)
            best_value = max(best_value, value)
            a = max(a, value)
            move.undo_update(board)
            if a > b:
                break
        return best_value

    @staticmethod
    def evaluate_state(board):
        value = board.get_value()
        return value


def parse_opening(raw_opening, openings):
    if not raw_opening:
        return

    if not raw_opening[0] in openings:
        openings[raw_opening[0]] = {}

    parse_opening(raw_opening[1:], openings[raw_opening[0]])

