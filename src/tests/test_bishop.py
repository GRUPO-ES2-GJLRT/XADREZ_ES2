# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.board import Board

moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestBishop(unittest.TestCase):

    def test_bishop_at_a1_can_move_in_diagonal_b2_to_h8(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/B7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_bishop_at_h8_can_move_in_diagonal_a1_to_g7(self):
        board = Board(new_game=False)
        board.load_fen("7B/8/8/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_bishop_at_a8_can_move_in_diagonal_a8_to_h1(self):
        board = Board(new_game=False)
        board.load_fen("B7/8/8/8/8/8/8/8 w kQkq - 0 1")
        pos = (0, 7)
        possible_moves = moves(pos, [
            (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_bishop_at_e5_can_move_in_diagonals_a1_to_h8_and_b8_to_h2(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/4B3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_B_at_a1_and_B_at_e5_can_move_to_b2_and_c3_and_d4(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/4B3/8/8/8/B7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 1), (2, 2), (3, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_bishop_at_e5_surround_by_allies_distance_2(self):
        board = Board(new_game=False)
        board.load_fen("8/2B3B1/8/4B3/8/2B3B1/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (3, 3), (5, 5),
            (3, 5), (5, 3),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_B_at_a1_and_an_b_at_e5_can_move_to_b2_and_c3_and_d4_and_e5(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/4b3/8/8/8/B7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 1), (2, 2), (3, 3), (4, 4)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
