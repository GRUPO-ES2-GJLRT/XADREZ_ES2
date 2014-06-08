# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


import unittest

from cython.importer import Board


moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestPawnMove(unittest.TestCase):

    def test_white_pawn_at_e5_can_move_to_e6(self):
        board = Board(False)
        board.load_fen("8/8/8/4P3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_e5_can_move_to_e4(self):
        board = Board(False)
        board.load_fen("8/8/8/4p3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 3)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_white_pawn_at_a2_can_move_to_a3_and_a4(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/P7/8 w kQkq - 0 1")
        pos = (0, 1)
        possible_moves = moves(pos, [(0, 2), (0, 3)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_a7_can_move_to_a6_and_a5(self):
        board = Board(False)
        board.load_fen("8/p7/8/8/8/8/8/8 w kQkq - 0 1")
        pos = (0, 6)
        possible_moves = moves(pos, [(0, 5), (0, 4)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_white_pawn_at_a2_with_piece_in_a4_can_move_to_a3(self):
        board = Board(False)
        board.load_fen("8/8/8/8/P7/8/P7/8 w kQkq - 0 1")
        pos = (0, 1)
        possible_moves = moves(pos, [(0, 2)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_a7_with_piece_in_a5_can_move_to_a6(self):
        board = Board(False)
        board.load_fen("8/p7/8/P7/8/8/8/8 w kQkq - 0 1")
        pos = (0, 6)
        possible_moves = moves(pos, [(0, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_white_pawn_at_a2_with_piece_in_a3_doesnt_have_any_moves(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/P7/P7/8 w kQkq - 0 1")
        pos = (0, 1)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_a7_with_piece_in_a6_doesnt_have_any_moves(self):
        board = Board(False)
        board.load_fen("8/p7/p7/8/8/8/8/8 w kQkq - 0 1")
        pos = (0, 6)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_white_pawn_at_e5_with_enemy_at_f6_can_move_to_e6_and_f6(self):
        board = Board(False)
        board.load_fen("8/8/5p2/4P3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 5), (5, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_white_pawn_at_e5_with_enemy_at_d6_can_move_to_e6_and_d6(self):
        board = Board(False)
        board.load_fen("8/8/3p2/4P3/8/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 5), (3, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_e5_with_enemy_at_d4_can_move_to_e4_and_d4(self):
        board = Board(False)
        board.load_fen("8/8/8/4p3/3P4/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 3), (3, 3)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_black_pawn_at_e5_with_enemy_at_f4_can_move_to_e4_and_f4(self):
        board = Board(False)
        board.load_fen("8/8/8/4p3/5P2/8/8/8 w kQkq - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 3), (5, 3)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestPawnEnPassant(unittest.TestCase):

    def test_P_at_e5_en_passant_with_enemy_at_f5_can_move_to_e6_and_f6(self):
        board = Board(False)
        board.load_fen("8/8/8/4Pp2/8/8/8/8 w kQkq f6 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 5), (5, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_P_at_e5_en_passant_with_enemy_at_d5_can_move_to_e6_and_d6(self):
        board = Board(False)
        board.load_fen("8/8/8/3pP3/8/8/8/8 w kQkq d6 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [(4, 5), (3, 5)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_p_at_e4_en_passant_with_enemy_at_d4_can_move_to_e3_and_d3(self):
        board = Board(False)
        board.load_fen("8/8/8/8/3Pp3/8/8/8 w kQkq d3 0 1")
        pos = (4, 3)
        possible_moves = moves(pos, [(4, 2), (3, 2)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_p_at_e4_en_passant_with_enemy_at_f4_can_move_to_e3_and_f3(self):
        board = Board(False)
        board.load_fen("8/8/8/8/4pP2/8/8/8 w kQkq f3 0 1")
        pos = (4, 3)
        possible_moves = moves(pos, [(4, 2), (5, 2)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestPawnPromotion(unittest.TestCase):

    def test_white_pawn_at_e7_should_be_promoted_at_e8(self):
        board = Board(False)
        board.load_fen("8/4P3/8/8/8/8/8/8 w kQkq f3 0 1")
        pos = (4, 6)
        possible_moves = moves(pos, [(4, 7)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
        board.move((4, 6), (4, 7), 5)
        self.assertEqual(board.at((4, 7)), "white queen")

    def test_white_pawn_at_e7_with_enemy_at_f8_should_be_promoted_at_f8(self):
        board = Board(False)
        board.load_fen("5p2/4P3/8/8/8/8/8/8 w kQkq f3 0 1")
        pos = (4, 6)
        possible_moves = moves(pos, [(4, 7), (5, 7)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
        board.move((4, 6), (5, 7), 5)
        self.assertEqual(board.at((5, 7)), "white queen")

    def test_black_pawn_at_e2_should_be_promoted_at_e1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/4p3/8 b kQkq f3 0 1")
        pos = (4, 1)
        possible_moves = moves(pos, [(4, 0)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
        board.move((4, 1), (4, 0), 5)
        self.assertEqual(board.at((4, 0)), "black queen")

    def test_black_pawn_at_e2_with_enemy_at_f1_should_be_promoted_at_f1(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/4p3/5P2 b kQkq f3 0 1")
        pos = (4, 1)
        possible_moves = moves(pos, [(4, 0), (5, 0)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)
        board.move((4, 1), (5, 0), 5)
        self.assertEqual(board.at((5, 0)), "black queen")


class TestPawnProtectsKing(unittest.TestCase):

    def test_pawn_can_move_if_it_doesnt_protect_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/8/4P3/8/3K4/8 w kQkq f3 0 1")
        pos = (4, 3)
        possible_moves = moves(pos, [(4, 4)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_pawn_can_move_to_protect_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/1q2K3/3P4/8 w kQkq f3 0 1")
        pos = (3, 1)
        possible_moves = moves(pos, [(3, 2)])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_pawn_cannot_move_if_it_is_protecting_the_king(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/q2PK4/8 w kQkq f3 0 1")
        pos = (3, 1)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestPawn(TestPawnMove,
               TestPawnEnPassant,
               TestPawnPromotion,
               TestPawnProtectsKing
               ):
    pass
