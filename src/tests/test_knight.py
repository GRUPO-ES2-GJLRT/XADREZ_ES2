# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import to_move_dict
from game_elements.board import Board
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import King


class TestKnightMoves(unittest.TestCase):

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


class TestKnightProtectsKing(unittest.TestCase):

    def test_knight_can_move_if_it_doesnt_protect_the_king(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
        King(board, WHITE, 3, 1)
        possible_moves = to_move_dict([
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3)
        ])
        attack = {}

        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_can_move_to_protect_the_king(self):
        board = Board(new_game=False)
        King(board, WHITE, 3, 3)
        Queen(board, BLACK, 0, 3)
        knight = Knight(board, WHITE, 4, 4)
        possible_moves = to_move_dict([(2, 3)])
        attack = {}
        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_can_move_to_protect_the_king2(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 3)
        Queen(board, BLACK, 2, 3)
        knight = Knight(board, WHITE, 4, 4)
        possible_moves = {}
        attack = to_move_dict([(2, 3)])
        self.assertEqual(knight.possible_moves(), (possible_moves, attack))

    def test_knight_cannot_move_if_it_is_protecting_the_king(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 3)
        Queen(board, BLACK, 0, 3)
        knight = Knight(board, WHITE, 2, 3)
        possible_moves = {}
        attack = {}
        self.assertEqual(knight.possible_moves(), (possible_moves, attack))


class TestKnight(TestKnightMoves, TestKnightProtectsKing):
    pass
