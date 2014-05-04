# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.board import Board

moves = lambda o, x: set((o, a) for a in x)
tuples = lambda x: set(a.tuple() for a in x)


class TestKingMove(unittest.TestCase):

    def test_king_at_e5_can_move_to_8_positions(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/4K3/8/8/8/8 w - - 0 1")
        pos = (4, 4)
        possible_moves = moves(pos, [
            (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (4, 5), (3, 5), (3, 4)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_king_at_a1_can_move_to_3_positions(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/K7 w - - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (1, 0), (1, 1)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_king_at_a1_and_ally_at_b2_can_move_to_2_positions(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/1P6/K7 w - - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1), (1, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_king_at_a1_and_allies_at_a2_and_b1_and_b2_no_moves(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/PP6/KP6 w - - 0 1")
        pos = (0, 0)
        possible_moves = set()
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_king_at_a1_and_enemy_at_c1_can_move_to_a2(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/K1k5 w - - 0 1")
        pos = (0, 0)
        possible_moves = moves(pos, [
            (0, 1),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_king_at_a2_and_enemy_rook_at_a8_cannot_move_to_a1(self):
        board = Board(new_game=False)
        board.load_fen("r7/8/8/8/8/8/K8/8 w - - 0 1")
        pos = (0, 1)
        possible_moves = moves(pos, [
            (1, 2),
            (1, 1),
            (1, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestKingCastling(unittest.TestCase):
    def test_kingside_white_castling(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/4K2R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0), (6, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_there_is_piece(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/4K1RR w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_there_is_piece2(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/4KR1R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/4K2R w - - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R3K2R w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0), (2, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        board.load_fen("5r2/8/8/8/8/8/8/4K2R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_final_hindered(self):
        board = Board(new_game=False)
        board.load_fen("6r1/8/8/8/8/8/8/4K2R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_white_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        board.load_fen("4r3/8/8/8/8/8/8/4K2R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (5, 1), (5, 0),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R3K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0), (2, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_there_is_piece(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/RP2K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_there_is_piece2(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R1P1K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_there_is_piece3(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R2PK3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 1), (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R3K3 w - - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("8/8/8/8/8/8/8/R3K2R w K - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0), (6, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_step_hindered(self):
        board = Board(new_game=False)
        board.load_fen("3r5/8/8/8/8/8/8/R3K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_final_hindered(self):
        board = Board(new_game=False)
        board.load_fen("2r5/8/8/8/8/8/8/R3K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_white_castling_is_not_possible_if_king_hindered(self):
        board = Board(new_game=False)
        board.load_fen("4r3/8/8/8/8/8/8/R3K3 w Q - 0 1")
        pos = (4, 0)
        possible_moves = moves(pos, [
            (3, 0), (3, 1), (5, 1), (5, 0)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling(self):
        board = Board(new_game=False)
        board.load_fen("4k2r/8/8/8/8/8/8/8 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7), (6, 7)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_there_is_piece(self):
        board = Board(new_game=False)
        board.load_fen("4k1pr/8/8/8/8/8/8/8 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_there_is_piece2(self):
        board = Board(new_game=False)
        board.load_fen("4kp1r/8/8/8/8/8/8/8 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("4k2r/8/8/8/8/8/8/8 w - - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("r3k2r/8/8/8/8/8/8/8 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7), (2, 7)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k2r/8/8/8/8/8/8/5R2 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_final_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k2r/8/8/8/8/8/8/6R1 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_kingside_black_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k2r/8/8/8/8/8/8/4R1 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling(self):
        board = Board(new_game=False)
        board.load_fen("r3k3/8/8/8/8/8/8/8 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7), (2, 7)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_there_is_piece(self):
        board = Board(new_game=False)
        board.load_fen("rp2k3/8/8/8/8/8/8/8 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_there_is_piece2(self):
        board = Board(new_game=False)
        board.load_fen("r1p1k3/8/8/8/8/8/8/8 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_there_is_piece3(self):
        board = Board(new_game=False)
        board.load_fen("r2pk3/8/8/8/8/8/8/8 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("r3k3/8/8/8/8/8/8/8 w - - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        board.load_fen("r3k2r/8/8/8/8/8/8/8 w k - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7), (6, 7)
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_step_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k3/8/8/8/8/8/8/3R4 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_final_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k3/8/8/8/8/8/8/2R5 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)

    def test_queenside_black_castling_is_not_possible_if_king_hindered(self):
        board = Board(new_game=False)
        board.load_fen("r3k3/8/8/8/8/8/8/4R3 w q - 0 1")
        pos = (4, 7)
        possible_moves = moves(pos, [
            (3, 7), (3, 6), (5, 6), (5, 7),
        ])
        self.assertEqual(tuples(board.piece_moves(pos)), possible_moves)


class TestKing(TestKingMove, TestKingCastling):
    pass
