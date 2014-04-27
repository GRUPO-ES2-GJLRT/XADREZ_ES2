# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from consts.colors import WHITE
from consts.moves import to_move_dict
from game_elements.board import Board
from pieces.knight import Knight


class TestKnight(unittest.TestCase):

    def test_knight_at_4_4_can_move_to_8_positions(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3)
        ])
        attack = {}

        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_can_move_to_2_positions(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (2, 1), (1, 2)
        ])
        attack = {}

        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_and_ally_at_2_1_can_move_to_1_position(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 0, 0)
        Knight(board, WHITE, 2, 1)
        possible_moves = to_move_dict([
            (1, 2)
        ])
        attack = {}

        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_at_0_0_and_allies_at_2_1_and_1_2_should_have_no_possible_moves(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 0, 0)
        Knight(board, WHITE, 2, 1)
        Knight(board, WHITE, 1, 2)
        possible_moves = {}
        attack = {}

        self.assertEqual(knight.possible_moves(), (possible_moves, attack))
