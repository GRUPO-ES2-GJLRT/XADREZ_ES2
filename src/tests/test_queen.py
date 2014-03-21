# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import to_move_dict

from pieces.board import Board
from pieces.queen import Queen

class TestQueen(unittest.TestCase):

    def test_queen_at_0_0_and_no_other_pieces_at_board_can_move_to_all_line_0_and_column_0_and_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_and_no_other_pieces_at_board_can_move_to_all_line_7_and_column_7_and_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 7, 7)
        possible_moves = to_move_dict([
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), 
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_4_4_and_no_other_pieces_at_board_can_move_to_all_line_4_and_column_4_and_diagonals_0_0_to_7_7_and_1_7_to_7_1(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allie_in_0_1_and_1_1_can_move_to_all_line_0(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        Queen(board, WHITE, 0, 1)
        Queen(board, WHITE, 1, 1)
        possible_moves = to_move_dict([
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allies_in_1_0_and_1_1_can_move_to_all_column_0(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        Queen(board, WHITE, 1, 0)
        Queen(board, WHITE, 1, 1)
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_ignored_allies_in_1_0_and_1_1_can_move_to_all_line_0_and_column_0_and_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        a1 = Queen(board, WHITE, 1, 0)
        a2 = Queen(board, WHITE, 1, 1)
        a1.ignored = True
        a2.ignored = True
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allies_in_1_0_and_0_1_can_move_to_all_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        Queen(board, WHITE, 1, 0)
        Queen(board, WHITE, 0, 1)
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)


    def test_queen_at_0_0_with_allies_in_2_0_and_2_2_can_move_to_all_column_0_and_positions_1_0_1_1(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        Queen(board, WHITE, 2, 0)
        Queen(board, WHITE, 2, 2)
        possible_moves = to_move_dict([
            (1, 0), (1, 1),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_with_allies_in_5_7_and_7_5_and_5_5_can_move_to_6_7_and_7_6_and_6_6(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 7, 7)
        Queen(board, WHITE, 5, 7)
        Queen(board, WHITE, 7, 5)
        Queen(board, WHITE, 5, 5)
        possible_moves = to_move_dict([
            (6, 7), (7, 6), (6, 6)
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_4_4_surrounded_by_allies_should_have_no_moves(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 4, 4)
        Queen(board, WHITE, 5, 4)
        Queen(board, WHITE, 4, 5)
        Queen(board, WHITE, 3, 4)
        Queen(board, WHITE, 4, 3)
        Queen(board, WHITE, 5, 5)
        Queen(board, WHITE, 3, 3)
        Queen(board, WHITE, 3, 5)
        Queen(board, WHITE, 5, 3)
        possible_moves = {}

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_with_enemies_in_5_7_and_7_5_and_5_5_can_move_to_6_7_and_7_6_and_5_7_and_7_5_and_6_6_and_5_5(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 7, 7)
        Queen(board, BLACK, 5, 7)
        Queen(board, BLACK, 7, 5)
        Queen(board, BLACK, 5, 5)
        possible_moves = to_move_dict([
            (6, 7), (7, 6),
            (5, 7), (7, 5),
            (6, 6), (5, 5), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_enemies_in_0_3_and_3_0_and_3_3_can_move_in_line_0_and_column_0_up_to_enemy_position_including_and_diagonal_0_0_to_3_3(self):
        board = Board(new_game=False)
        queen = Queen(board, WHITE, 0, 0)
        Queen(board, BLACK, 0, 3)
        Queen(board, BLACK, 3, 0)
        Queen(board, BLACK, 3, 3)
        possible_moves = to_move_dict([
            (0, 1), (0, 2), (0, 3),
            (1, 0), (2, 0), (3, 0),
            (1, 1), (2, 2), (3, 3)
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)