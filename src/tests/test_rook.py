# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.importer import Board

moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestRook(unittest.TestCase):

    def test_R_at_a1_can_move_to_all_A_and_1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/R7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_R_at_H8_can_move_to_all_H_and_8(self):
        board = Board(False)
        board.load_fen("7R/8/8/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_R_at_e5_can_move_to_all_E_and_5(self):
        board = Board(False)
        board.load_fen("8/8/8/4R3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_a1_with_ally_in_a2_can_move_to_all_1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/R7/R7 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_a1_with_ally_in_b1_can_move_to_all_A(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/RR6 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_a1_with_ally_in_c1_can_move_to_all_A_and_b1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/R1R5 w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (1, 0),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_h8_with_allies_in_f8_and_h6_can_move_to_g8_and_h7(self):
        board = Board(False)
        board.load_fen("5R1R/8/7R/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (6, 7), (7, 6)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_e5_surrounded_by_allies_should_have_no_moves(self):
        board = Board(False)
        board.load_fen("8/8/4R3/3RRR2/4R3/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_rook_at_h8_with_enemies_in_f8_h6_can_move_to_g8_h7_f8_h6(self):
        board = Board(False)
        board.load_fen("5r1R/8/7r/8/8/8/8/8 w kQkq - 0 1")
        pos = (7, 7)
        possible_moves = moves(pos, [
            (5, 7), (7, 5),
            (6, 7), (7, 6)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_R_at_a1_and_r_at_d1_and_a4_cmup_to_enemy_position_including(self):
        board = Board(False)
        board.load_fen("8/8/8/8/r7/8/8/R2r w kQkq - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (0, 2),
            (1, 0), (2, 0),
            (0, 3), (3, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
