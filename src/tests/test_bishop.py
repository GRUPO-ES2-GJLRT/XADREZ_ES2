# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from pieces.board import Board
from pieces.bishop import Bishop

class TestBishop(unittest.TestCase):

    def test_bishop_at_0_0_and_no_other_pieces_at_board_can_move_in_diagonal_1_1_to_7_7(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 0, 0)
        possible_moves = set([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_7_7_and_no_other_pieces_at_board_can_move_in_diagonal_0_0_to_6_6(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 7, 7)
        possible_moves = set([
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), 
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_0_7_and_no_other_pieces_at_board_can_move_in_diagonal_0_7_to_7_0(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 0, 7)
        possible_moves = set([
            (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0) 
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_4_4_and_no_other_pieces_at_board_can_move_in_diagonals_0_0_to_7_7_and_1_7_to_7_1(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 4, 4)
        possible_moves = set([
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1)
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_0_0_and_an_ally_in_4_4_can_move_to_1_1_and_2_2_and_3_3(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 0, 0)
        Bishop(board, 'white', 4, 4)
        possible_moves = set([
            (1, 1), (2, 2), (3, 3)
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_4_4_surround_by_allies_with_distance_2_has_4_possible_moves(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 4, 4)
        Bishop(board, 'white', 2, 2)
        Bishop(board, 'white', 6, 6)
        Bishop(board, 'white', 2, 6)
        Bishop(board, 'white', 6, 2)
        possible_moves = set([
            (3, 3), (5, 5),
            (3, 5), (5, 3),
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)

    def test_bishop_at_0_0_and_an_enemy_in_4_4_can_move_to_1_1_and_2_2_and_3_3_and_4_4(self):
        board = Board(new_game=False)
        bishop = Bishop(board, 'white', 0, 0)
        Bishop(board, 'black', 4, 4)
        possible_moves = set([
            (1, 1), (2, 2), (3, 3), (4, 4),
        ])

        self.assertEqual(bishop.possible_moves(), possible_moves)
