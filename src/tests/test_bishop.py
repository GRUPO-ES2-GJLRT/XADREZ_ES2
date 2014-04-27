# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import to_move_dict
from game_elements.board import Board
from pieces.bishop import Bishop


class TestBishop(unittest.TestCase):

    def test_bishop_at_0_0_and_no_other_pieces_at_board_can_move_in_diagonal_1_1_to_7_7(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 0, 0)
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_7_7_and_no_other_pieces_at_board_can_move_in_diagonal_0_0_to_6_6(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 7, 7)
        possible_moves = to_move_dict([
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_0_7_and_no_other_pieces_at_board_can_move_in_diagonal_0_7_to_7_0(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 0, 7)
        possible_moves = to_move_dict([
            (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_4_4_and_no_other_pieces_at_board_can_move_in_diagonals_0_0_to_7_7_and_1_7_to_7_1(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
            (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1),
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_0_0_and_an_ally_in_4_4_can_move_to_1_1_and_2_2_and_3_3(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 0, 0)
        Bishop(board, WHITE, 4, 4)
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3)
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_0_0_and_an_ignored_ally_in_4_4_can_move_in_diagonal_1_1_to_7_7(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 0, 0)
        ally = Bishop(board, WHITE, 4, 4)
        ally.ignored = True
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_4_4_surround_by_allies_with_distance_2_has_4_possible_moves(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 4, 4)
        Bishop(board, WHITE, 2, 2)
        Bishop(board, WHITE, 6, 6)
        Bishop(board, WHITE, 2, 6)
        Bishop(board, WHITE, 6, 2)
        possible_moves = to_move_dict([
            (3, 3), (5, 5),
            (3, 5), (5, 3),
        ])
        attack = {}

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))

    def test_bishop_at_0_0_and_an_enemy_in_4_4_can_move_to_1_1_and_2_2_and_3_3_and_4_4(self):
        board = Board(new_game=False)
        bishop = Bishop(board, WHITE, 0, 0)
        Bishop(board, BLACK, 4, 4)
        possible_moves = to_move_dict([
            (1, 1), (2, 2), (3, 3),
        ])
        attack = to_move_dict([(4, 4)])

        self.assertEqual(bishop.possible_moves(), (possible_moves, attack))
