# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from consts.colors import WHITE, BLACK

from pieces.board import Board
from pieces.knight import Knight
from pieces.king import King
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.pawn import Pawn


class TestBoardValid(unittest.TestCase):

    def test_valid_4_4_should_be_true(self):
        board = Board(new_game=False)
        self.assertTrue(board.valid((4, 4)))

    def test_valid_negative1_4_should_be_false(self):
        board = Board(new_game=False)
        self.assertFalse(board.valid((-1, 4)))

    def test_valid_4_negative1_should_be_false(self):
        board = Board(new_game=False)
        self.assertFalse(board.valid((4, -1)))

    def test_valid_8_4_should_be_false(self):
        board = Board(new_game=False)
        self.assertFalse(board.valid((8, 4)))

    def test_valid_4_8_should_be_false(self):
        board = Board(new_game=False)
        self.assertFalse(board.valid((4, 8)))
        

class TestBoardGetItem(unittest.TestCase):

    def test_get_from_valid_position_without_piece_returns_none(self):
        board = Board(new_game=False)
        self.assertEqual(board[(4, 4)], None)

    def test_get_from_valid_position_with_piece_returns_piece(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
        self.assertEqual(board[(4, 4)], knight)

    def test_get_from_invalid_position_returns_none(self):
        board = Board(new_game=False)
        self.assertEqual(board[(-4, 4)], None)


class TestBoardNewGame(unittest.TestCase):

    def test_create_board_new_game_false(self):
        board = Board(new_game=False)
        for x in xrange(8):
            for y in xrange(8):
                self.assertEqual(board[(x, y)], None)


    def test_create_board_new_game_true(self):
        board = Board(new_game=True)
        # Pawn
        for x in xrange(8):
            black_pawn = board[(x, 6)]
            white_pawn = board[(x, 1)]
            self.assertEqual(black_pawn.color, BLACK)
            self.assertEqual(white_pawn.color, WHITE)
            self.assertEqual(black_pawn.__class__, Pawn)
            self.assertEqual(white_pawn.__class__, Pawn)
        # Rook
        white_rooks = [board[(0, 0)], board[(7, 0)]]
        for rook in white_rooks:
            self.assertEqual(rook.color, WHITE)
            self.assertEqual(rook.__class__, Rook)
        black_rooks = [board[(0, 7)], board[(7, 7)]]
        for rook in black_rooks:
            self.assertEqual(rook.color, BLACK)
            self.assertEqual(rook.__class__, Rook)
        # Knight
        white_knights = [board[(1, 0)], board[(6, 0)]]
        for knight in white_knights:
            self.assertEqual(knight.color, WHITE)
            self.assertEqual(knight.__class__, Knight)
        black_knights = [board[(1, 7)], board[(6, 7)]]
        for knight in black_knights:
            self.assertEqual(knight.color, BLACK)
            self.assertEqual(knight.__class__, Knight)
        # Bishop
        white_bishops = [board[(2, 0)], board[(5, 0)]]
        for bishop in white_bishops:
            self.assertEqual(bishop.color, WHITE)
            self.assertEqual(bishop.__class__, Bishop)
        black_bishops = [board[(2, 7)], board[(5, 7)]]
        for bishop in black_bishops:
            self.assertEqual(bishop.color, BLACK)
            self.assertEqual(bishop.__class__, Bishop)
        # Queen
        white_queen = board[(3, 0)]
        self.assertEqual(white_queen.color, WHITE)
        self.assertEqual(white_queen.__class__, Queen)
        black_queen = board[(3, 7)]
        self.assertEqual(black_queen.color, BLACK)
        self.assertEqual(black_queen.__class__, Queen)
        # King
        white_king = board[(4, 0)]
        self.assertEqual(white_king.color, WHITE)
        self.assertEqual(white_king.__class__, King)
        black_king = board[(4, 7)]
        self.assertEqual(black_king.color, BLACK)
        self.assertEqual(black_king.__class__, King)


class TestBoardRemove(unittest.TestCase):

    def test_remove_white_piece_at_4_4(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
        self.assertEqual(board[(4, 4)], knight)
        self.assertEqual(board.pieces[WHITE], [knight])
        board.remove((4, 4))
        self.assertEqual(board[(4, 4)], None)
        self.assertEqual(board.pieces[WHITE], [])

    def test_remove_black_piece_at_0_6(self):
        board = Board(new_game=True)
        self.assertEqual(board[(0, 6)].name(), "pawn")
        self.assertEqual(len(board.pieces[WHITE]), 16)
        self.assertEqual(len(board.pieces[BLACK]), 16)
        board.remove((0, 6))
        self.assertEqual(board[(0, 6)], None)
        self.assertEqual(len(board.pieces[WHITE]), 16)
        self.assertEqual(len(board.pieces[BLACK]), 15)

class TestBoardHindered(unittest.TestCase):

    def test_hindered_in_a_board_with_just_a_knight(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
        expected_hindered_white = set([
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3) 
        ])
        expected_hindered_black = set()
        self.assertEqual(board.hindered(WHITE), expected_hindered_white)
        self.assertEqual(board.hindered(BLACK), expected_hindered_black)


    def test_hindered_in_a_new_game(self):
        board = Board(new_game=True)
        expected_hindered_white = set([
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2) 
        ])
        expected_hindered_black = set([
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5) 
        ])
        self.assertEqual(board.hindered(WHITE), expected_hindered_white)
        self.assertEqual(board.hindered(BLACK), expected_hindered_black)


class TestBoard(TestBoardValid, TestBoardGetItem, TestBoardNewGame, TestBoardRemove, TestBoardHindered):
    pass