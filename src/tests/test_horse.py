# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from pieces.board import Board
from pieces.horse import Horse

class TestHorse(unittest.TestCase):

    def test_horse_at_4_4_can_move_to_8_positions(self):
        board = Board(new_game=False)
        horse = Horse(board, 'white', 4, 4)
        possible_moves = set([
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3) 
        ])

        self.assertEqual(horse.possible_moves(), possible_moves)

    def test_horse_at_0_0_can_move_to_2_positions(self):
        board = Board(new_game=False)
        horse = Horse(board, 'white', 0, 0)
        possible_moves = set([
            (2, 1), (1, 2)
        ])

        self.assertEqual(horse.possible_moves(), possible_moves)

    def test_horse_at_0_0_and_ally_at_2_1_can_move_to_1_position(self):
        board = Board(new_game=False)
        horse = Horse(board, 'white', 0, 0)
        Horse(board, 'white', 2, 1)
        possible_moves = set([
            (1, 2)
        ])

        self.assertEqual(horse.possible_moves(), possible_moves)

    def test_horse_at_0_0_and_allies_at_2_1_and_1_2_should_have_no_possible_moves(self):
        board = Board(new_game=False)
        horse = Horse(board, 'white', 0, 0)
        Horse(board, 'white', 2, 1)
        Horse(board, 'white', 1, 2)
        possible_moves = set()

        self.assertEqual(horse.possible_moves(), possible_moves)
