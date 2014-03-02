# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from pieces.board import Board
from pieces.tower import Tower

class TestTower(unittest.TestCase):

    def test_tower_at_0_0_and_no_other_pieces_at_board_can_move_to_all_line_0_and_column_0(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 0, 0)
        possible_moves = set([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_7_7_and_no_other_pieces_at_board_can_move_to_all_line_7_and_column_7(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 7, 7)
        possible_moves = set([
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), 
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_4_4_and_no_other_pieces_at_board_can_move_to_all_line_4_and_column_4(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 4, 4)
        possible_moves = set([
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), 
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_0_0_with_ally_in_0_1_can_move_to_all_line_0(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 0, 0)
        Tower(board, 'white', 0, 1)
        possible_moves = set([
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_0_0_with_ally_in_1_0_can_move_to_all_column_0(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 0, 0)
        Tower(board, 'white', 1, 0)
        possible_moves = set([
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_0_0_with_ally_in_2_0_can_move_to_all_column_0_and_position_1_0(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 0, 0)
        Tower(board, 'white', 2, 0)
        possible_moves = set([
            (1, 0),
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_7_7_with_allies_in_5_7_and_7_5_can_move_to_6_7_and_7_6(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 7, 7)
        Tower(board, 'white', 5, 7)
        Tower(board, 'white', 7, 5)
        possible_moves = set([
            (6, 7), (7, 6)
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_4_4_surrounded_by_allies_should_have_no_moves(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 4, 4)
        Tower(board, 'white', 5, 4)
        Tower(board, 'white', 4, 5)
        Tower(board, 'white', 3, 4)
        Tower(board, 'white', 4, 3)
        possible_moves = set()

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_7_7_with_enemies_in_5_7_and_7_5_can_move_to_6_7_and_7_6_and_5_7_and_7_5(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 7, 7)
        Tower(board, 'black', 5, 7)
        Tower(board, 'black', 7, 5)
        possible_moves = set([
            (6, 7), (7, 6),
            (5, 7), (7, 5), 
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)

    def test_tower_at_0_0_with_enemies_in_0_3_and_3_0_can_move_in_line_0_and_column_0_up_to_enemy_position_including(self):
        board = Board(new_game=False)
        tower = Tower(board, 'white', 0, 0)
        Tower(board, 'black', 0, 3)
        Tower(board, 'black', 3, 0)
        possible_moves = set([
            (0, 1), (0, 2), (0, 3),
            (1, 0), (2, 0), (3, 0),
        ])

        self.assertEqual(tower.possible_moves(), possible_moves)