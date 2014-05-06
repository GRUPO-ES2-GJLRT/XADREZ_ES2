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
            self.do_move(self.minmax_move(2))

        elif self.level == HARD:
            raise Exception

        elif self.level == SUCH_HARD_MUCH_DIFFICULT:
            raise Exception

    def confirm_draw(self):
        self.chess.deny_draw(self)

    def minmax_move(self, depth):
        a = float('-inf')
        b = float('inf')

        node = Node(self.temp_board)
        node._value = self.evaluate_state(node)
        max_move = None
        for child in node.children():
            value = self.minmax_alpha_beta_prunning(
                child, depth - 1, a, b, False)
            if a < value:
                a = value
                max_move = child.move
        node._value = a
        return max_move

    def minmax_alpha_beta_prunning(self, node, depth, a, b, maximizing_player):
        if depth == 0 or node.is_terminal():
            node.value = self.evaluate_state(node)
            return node.value

        if maximizing_player:
            for child in node.children():
                a = max(
                    a,
                    self.minmax_alpha_beta_prunning(child,
                                                    depth - 1, a, b, False)
                )
                if b <= a:
                    break
            node.value = a
            return a
        else:
            for child in node.children():
                b = min(
                    b,
                    self.minmax_alpha_beta_prunning(child,
                                                    depth - 1, a, b, True)
                )
                if b <= a:
                    break
            node.value = b
            return b

    @staticmethod
    def evaluate_state(node):
        value = node.board.get_value()

        if node.board.color() == WHITE:
            return value
        return value * -1


class Node(object):

    def __init__(self, board, move=None):
        self.board = board
        self.move = move
        self.moves = self.board.possible_moves(board.color())
        self._value = 0.0
        self.color = self.board.color()
        self.childs = []
        self.done = False

    @property
    def value(self):
        """ Return the piece position x, y """
        return self._value

    @value.setter
    def value(self, value):
        """ sets x, y """
        self._value = value
        self.done = True
        del self.moves
        del self.board

    def is_terminal(self):
        return ((not self.moves) or
                self.board.status(self.moves) in [CHECKMATE, STALEMATE])

    def children(self):
        for move in self.moves:
            nboard = self.board.clone()
            move.do(nboard)
            yield Node(nboard, move=move)


def parse_opening(raw_opening, openings):
    if not raw_opening:
        return

    if not raw_opening[0] in openings:
        openings[raw_opening[0]] = {}

    parse_opening(raw_opening[1:], openings[raw_opening[0]])

