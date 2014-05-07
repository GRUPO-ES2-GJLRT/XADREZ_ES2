# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.board import Board

moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestKnightMoves(unittest.TestCase):

    def test_knight_at_e5_can_move_to_8_positions(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_at_a1_can_move_to_2_positions(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/N7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (2, 1), (1, 2)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_at_a1_and_ally_at_c2_can_move_to_1_position(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/2N5/N7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 2)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_at_a1_and_allies_at_c2_and_b3_should_have_no_moves(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/1N6/2N5/N7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestKnightProtectsKing(unittest.TestCase):

    def test_knight_can_move_if_it_doesnt_protect_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/8/8/3K4/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_can_move_to_protect_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/q2K5/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (2, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_can_move_to_protect_the_king2(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/2q1K3/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (2, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_knight_cannot_move_if_it_is_protecting_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/2qNK3/8/8/8 w kQkq - 0 1")
        pos = (3, 3)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestKnight(TestKnightMoves, TestKnightProtectsKing):
    pass
