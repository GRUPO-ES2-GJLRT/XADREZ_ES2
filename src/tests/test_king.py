# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from pieces.board import Board
from pieces.king import King

class TestKing(unittest.TestCase):

    def test_king_at_4_4_can_move_to_8_positions(self):
        board = Board(new_game=False)
        king = King(board, 'white', 4, 4)
        possible_moves = set([
            (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (4, 5), (3, 5), (3, 4) 
        ])

        self.assertEqual(king.possible_moves(), possible_moves)

    def test_king_at_0_0_can_move_to_3_positions(self):
        board = Board(new_game=False)
        king = King(board, 'white', 0, 0)
        possible_moves = set([
            (0, 1), (1, 0), (1, 1)
        ])

        self.assertEqual(king.possible_moves(), possible_moves)

    def test_knight_at_0_0_and_ally_at_1_1_can_move_to_2_positions(self):
        board = Board(new_game=False)
        king = King(board, 'white', 0, 0)
        King(board, 'white', 1, 1)
        possible_moves = set([
            (0, 1), (1, 0), 
        ])

        self.assertEqual(king.possible_moves(), possible_moves)

    def test_knight_at_0_0_and_allies_at_0_1_and_1_0_and_1_1_should_have_no_possible_moves(self):
        board = Board(new_game=False)
        king = King(board, 'white', 0, 0)
        King(board, 'white', 0, 1)
        King(board, 'white', 1, 0)
        King(board, 'white', 1, 1)
        possible_moves = set()

        self.assertEqual(king.possible_moves(), possible_moves)
