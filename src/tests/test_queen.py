# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import unittest

from cython.board import Board


moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestQueen(unittest.TestCase):

    def test_queen_at_a1_and_can_move_to_A_and_1_and_diagonal_a1_to_h8(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/Q7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_h8_and_can_move_to_H_and_8_and_diagonal_a1_to_h8(self):
        board = Board(False)
        board.load_fen("7Q/8/8/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_e5_and_can_move_to_E_and_5_diag_a1_h8_and_b8_h2(self):
        board = Board(False)
        board.load_fen("8/8/8/4Q3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_a1_with_allie_in_a2_and_b2_can_move_to_1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/QQ6/Q7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_a1_with_allies_in_b1_and_b2_can_move_to_A(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/1Q6/QQ w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_a1_with_allies_in_b1_a2_can_move_to_all_diag_a1_h8(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/Q7/QQ6 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_a1_with_allies_in_c1_c3_can_move_to_A_and_b1_b2(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/2Q5/8/Q1Q5 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 0), (1, 1),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_h8_with_allies_in_f8_h6_f6_can_move_to_g8_h7_g7(self):
        board = Board(False)
        board.load_fen("5Q1Q/8/5Q1Q/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (6, 7), (7, 6), (6, 6)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_e5_surrounded_by_allies_should_have_no_moves(self):
        board = Board(False)
        board.load_fen("8/8/3QQQ2/3QQQ2/3QQQ2/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queen_at_h8_with_enemies_in_f8_h6_f6_m_to_g8_h7_f8_h6_g7_f6(self):
        board = Board(False)
        board.load_fen("5q1Q/8/5q1q/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (6, 7), (7, 6),
            (6, 6),
            (5, 7), (7, 5), (5, 5),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_Q_at_a1_with_q_at_a4_d1_d4_can_move_up_to_enemy(self):
        board = Board(False)
        board.load_fen("8/8/8/8/q2q4/8/8/Q2q4 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (0, 2),
            (1, 0), (2, 0),
            (1, 1), (2, 2),
            (0, 3), (3, 0), (3, 3)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
