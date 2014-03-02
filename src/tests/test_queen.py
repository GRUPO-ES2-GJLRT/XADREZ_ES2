# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from pieces.board import Board
from pieces.queen import Queen

class TestQueen(unittest.TestCase):

    def test_queen_at_0_0_and_no_other_pieces_at_board_can_move_to_all_line_0_and_column_0_and_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        possible_moves = set([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_and_no_other_pieces_at_board_can_move_to_all_line_7_and_column_7_and_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 7, 7)
        possible_moves = set([
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), 
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_4_4_and_no_other_pieces_at_board_can_move_to_all_line_4_and_column_4_and_diagonals_0_0_to_7_7_and_1_7_to_7_1(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 4, 4)
        possible_moves = set([
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allie_in_0_1_and_1_1_can_move_to_all_line_0(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        Queen(board, 'white', 0, 1)
        Queen(board, 'white', 1, 1)
        possible_moves = set([
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allies_in_1_0_and_1_1_can_move_to_all_column_0(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        Queen(board, 'white', 1, 0)
        Queen(board, 'white', 1, 1)
        possible_moves = set([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_allies_in_1_0_and_0_1_can_move_to_all_diagonal_0_0_to_7_7(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        Queen(board, 'white', 1, 0)
        Queen(board, 'white', 0, 1)
        possible_moves = set([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)


    def test_queen_at_0_0_with_allies_in_2_0_and_2_2_can_move_to_all_column_0_and_positions_1_0_1_1(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        Queen(board, 'white', 2, 0)
        Queen(board, 'white', 2, 2)
        possible_moves = set([
            (1, 0), (1, 1),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_with_allies_in_5_7_and_7_5_and_5_5_can_move_to_6_7_and_7_6_and_6_6(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 7, 7)
        Queen(board, 'white', 5, 7)
        Queen(board, 'white', 7, 5)
        Queen(board, 'white', 5, 5)
        possible_moves = set([
            (6, 7), (7, 6), (6, 6)
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_4_4_surrounded_by_allies_should_have_no_moves(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 4, 4)
        Queen(board, 'white', 5, 4)
        Queen(board, 'white', 4, 5)
        Queen(board, 'white', 3, 4)
        Queen(board, 'white', 4, 3)
        Queen(board, 'white', 5, 5)
        Queen(board, 'white', 3, 3)
        Queen(board, 'white', 3, 5)
        Queen(board, 'white', 5, 3)
        possible_moves = set()

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_7_7_with_enemies_in_5_7_and_7_5_and_5_5_can_move_to_6_7_and_7_6_and_5_7_and_7_5_and_6_6_and_5_5(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 7, 7)
        Queen(board, 'black', 5, 7)
        Queen(board, 'black', 7, 5)
        Queen(board, 'black', 5, 5)
        possible_moves = set([
            (6, 7), (7, 6),
            (5, 7), (7, 5),
            (6, 6), (5, 5), 
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)

    def test_queen_at_0_0_with_enemies_in_0_3_and_3_0_and_3_3_can_move_in_line_0_and_column_0_up_to_enemy_position_including_and_diagonal_0_0_to_3_3(self):
        board = Board(new_game=False)
        queen = Queen(board, 'white', 0, 0)
        Queen(board, 'black', 0, 3)
        Queen(board, 'black', 3, 0)
        Queen(board, 'black', 3, 3)
        possible_moves = set([
            (0, 1), (0, 2), (0, 3),
            (1, 0), (2, 0), (3, 0),
            (1, 1), (2, 2), (3, 3)
        ])

        self.assertEqual(queen.possible_moves(), possible_moves)