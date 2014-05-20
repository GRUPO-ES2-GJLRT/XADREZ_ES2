# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
from os import path
import threading
from collections import Counter
from time import sleep
from consts.moves import (
    CHECKMATE, STALEMATE
)
from consts.end_game import END_GAME, PAUSE
from consts.pieces import PAWN, KING
from consts.colors import WHITE, BLACK
from .player import Player, END
from cython.constants import ILLEGAL, LEGAL, EMPTY
from cython.board import move_key
from cython.functions import *

PLAYER = None
RANDOM = 0
SEMI_RANDOM = 1
EASY = 2
MEDIUM = 3
HARD = 4

DEPTH = {
    EASY: 2,
    MEDIUM: 4,
    HARD: 5,
}


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
        openings_file = path.abspath(
            path.join(sys.argv[0], '..', '..', 'src', 'openings.dat')
        )
        with open(openings_file) as _file:
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

    def do_opening_move(self):
        chosen_move = random.choice(self.openings.keys())
        chess = self.chess
        while chess.state == PAUSE:
            self.try_to_exit_thread_loop()
            pass
        if not chosen_move:
            return

        self.openings = self.openings[chosen_move]
        self.select(p0x88_to_tuple(chess_notation_to_0x88(chosen_move[:2])))
        self.play(p0x88_to_tuple(chess_notation_to_0x88(chosen_move[-2:])))
        chess.do_jit_draw()

    def do_move(self, chosen_move):
        chess = self.chess
        while chess.state == PAUSE:
            self.try_to_exit_thread_loop()
            pass
        if not chosen_move:
            return
        tup = chosen_move.tuple()
        self.select(tup[0])
        self.play(tup[1])
        chess.do_jit_draw()

    def try_to_exit_thread_loop(self):
        if (self.state == END or self.chess.state in END_GAME
                or not self.chess.game.running):
            sys.exit(0)

    def ai_move(self):
        if (self.state == END or self.chess.state in END_GAME):
            return

        if self.level == RANDOM:
            moves = list(self.temp_board.possible_moves(self.color))

            while not moves:
                self.try_to_exit_thread_loop()
                moves = list(self.temp_board.possible_moves(self.color))

            self.do_move(random.choice(moves))

        elif self.level == SEMI_RANDOM:
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

        elif self.level in [EASY, MEDIUM, HARD]:
            if self.openings:
                self.do_opening_move()
            else:
                self.do_move(self.negamax_move(DEPTH[self.level]))


    def confirm_draw(self):
        self.chess.deny_draw(self)

    def negamax_move(self, depth):
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

