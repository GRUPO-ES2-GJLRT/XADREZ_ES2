# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import to_move_dict
from game_elements.board import Board
from pieces.rook import Rook

class TestRook(unittest.TestCase):

    def test_rook_at_0_0_and_no_other_pieces_at_board_can_move_to_all_line_0_and_column_0(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_7_7_and_no_other_pieces_at_board_can_move_to_all_line_7_and_column_7(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 7, 7)
        possible_moves = to_move_dict([
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), 
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_4_4_and_no_other_pieces_at_board_can_move_to_all_line_4_and_column_4(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), 
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_0_0_with_ally_in_0_1_can_move_to_all_line_0(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 0, 1)
        possible_moves = to_move_dict([
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_0_0_with_ignored_ally_in_0_1_can_move_to_all_line_0_and_column_0(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        ally = Rook(board, WHITE, 0, 1)
        ally.ignored = True
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])
        
        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_0_0_with_ally_in_1_0_can_move_to_all_column_0(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 1, 0)
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_0_0_with_ally_in_2_0_can_move_to_all_column_0_and_position_1_0(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        Rook(board, WHITE, 2, 0)
        possible_moves = to_move_dict([
            (1, 0),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_7_7_with_allies_in_5_7_and_7_5_can_move_to_6_7_and_7_6(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 7, 7)
        Rook(board, WHITE, 5, 7)
        Rook(board, WHITE, 7, 5)
        possible_moves = to_move_dict([
            (6, 7), (7, 6)
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_4_4_surrounded_by_allies_should_have_no_moves(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 4, 4)
        Rook(board, WHITE, 5, 4)
        Rook(board, WHITE, 4, 5)
        Rook(board, WHITE, 3, 4)
        Rook(board, WHITE, 4, 3)
        possible_moves = {}

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_7_7_with_enemies_in_5_7_and_7_5_can_move_to_6_7_and_7_6_and_5_7_and_7_5(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 7, 7)
        Rook(board, BLACK, 5, 7)
        Rook(board, BLACK, 7, 5)
        possible_moves = to_move_dict([
            (6, 7), (7, 6),
            (5, 7), (7, 5), 
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)

    def test_rook_at_0_0_with_enemies_in_0_3_and_3_0_can_move_in_line_0_and_column_0_up_to_enemy_position_including(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 0, 0)
        Rook(board, BLACK, 0, 3)
        Rook(board, BLACK, 3, 0)
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3),
            (1, 0), (2, 0), (3, 0),
        ])

        self.assertEqual(rook.possible_moves(), possible_moves)