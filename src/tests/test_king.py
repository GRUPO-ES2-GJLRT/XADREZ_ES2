# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import KINGSIDE_CASTLING, QUEENSIDE_CASTLING, to_move_dict
from game_elements.board import Board
from pieces.king import King
from pieces.rook import Rook


class TestKingMove(unittest.TestCase):

    def test_king_at_4_4_can_move_to_8_positions(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (4, 5), (3, 5), (3, 4)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_king_at_0_0_can_move_to_3_positions(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (0, 1), (1, 0), (1, 1)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_and_ally_at_1_1_can_move_to_2_positions(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 0, 0)
        King(board, WHITE, 1, 1)
        possible_moves = to_move_dict([
            (0, 1), (1, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_and_allies_at_0_1_and_1_0_and_1_1_should_have_no_possible_moves(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 0, 0)
        King(board, WHITE, 0, 1)
        King(board, WHITE, 1, 0)
        King(board, WHITE, 1, 1)
        possible_moves = {}
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_and_enemy_at_2_0_can_move_to_0_1(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 0, 0)
        King(board, BLACK, 2, 0)
        possible_moves = to_move_dict([
            (0, 1),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))


class TestKingCastling(unittest.TestCase):
    def test_kingside_white_castling(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
            (6, 0, KINGSIDE_CASTLING)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_there_is_piece_in_between(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        Rook(board, WHITE, 6, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_there_is_piece_in_between2(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        Rook(board, WHITE, 5, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        king.has_moved = True
        Rook(board, WHITE, 7, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        rook = Rook(board, WHITE, 7, 0)
        rook.has_moved = True
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        Rook(board, BLACK, 5, 7)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_final_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        Rook(board, BLACK, 6, 7)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_white_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 7, 0)
        Rook(board, BLACK, 4, 7)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
            (2, 0, QUEENSIDE_CASTLING)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_there_is_piece_in_between(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 1, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_there_is_piece_in_between2(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 2, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_there_is_piece_in_between3(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 3, 0)
        possible_moves = to_move_dict([
            (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        king.has_moved = True
        Rook(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        rook = Rook(board, WHITE, 0, 0)
        rook.has_moved = True
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, BLACK, 3, 7)
        possible_moves = to_move_dict([
            (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_final_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, BLACK, 2, 7)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (4, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_white_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Rook(board, WHITE, 0, 0)
        Rook(board, BLACK, 4, 7)
        possible_moves = to_move_dict([
            (3, 0), (3, 1), (5, 1), (5, 0),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
            (6, 7, KINGSIDE_CASTLING)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_there_is_piece_in_between(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        Rook(board, BLACK, 6, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_there_is_piece_in_between2(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        Rook(board, BLACK, 5, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        king.has_moved = True
        Rook(board, BLACK, 7, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        rook = Rook(board, BLACK, 7, 7)
        rook.has_moved = True
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        Rook(board, WHITE, 5, 0)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_final_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        Rook(board, WHITE, 6, 0)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_kingside_black_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 7, 7)
        Rook(board, WHITE, 4, 0)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
            (2, 7, QUEENSIDE_CASTLING)
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_there_is_piece_in_between(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, BLACK, 1, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_there_is_piece_in_between2(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, BLACK, 2, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_there_is_piece_in_between3(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, BLACK, 3, 7)
        possible_moves = to_move_dict([
            (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_king_has_moved(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        king.has_moved = True
        Rook(board, BLACK, 0, 7)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_rook_has_moved(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        rook = Rook(board, BLACK, 0, 7)
        rook.has_moved = True
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_step_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, WHITE, 3, 0)
        possible_moves = to_move_dict([
            (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_final_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, WHITE, 2, 0)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (4, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))

    def test_queenside_black_castling_is_not_possible_if_king_is_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        Rook(board, BLACK, 0, 7)
        Rook(board, WHITE, 4, 0)
        possible_moves = to_move_dict([
            (3, 7), (3, 6), (5, 6), (5, 7),
        ])
        attack = {}

        self.assertEqual(king.possible_moves(), (possible_moves, attack))


class TestKing(TestKingMove, TestKingCastling):
    pass
