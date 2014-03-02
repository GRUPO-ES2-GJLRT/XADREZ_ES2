# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
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
        knight = Knight(board, 'white', 4, 4)
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
            self.assertEqual(black_pawn.color, 'black')
            self.assertEqual(white_pawn.color, 'white')
            self.assertEqual(black_pawn.__class__, Pawn)
            self.assertEqual(white_pawn.__class__, Pawn)
        # Rook
        white_rooks = [board[(0, 0)], board[(7, 0)]]
        for rook in white_rooks:
            self.assertEqual(rook.color, 'white')
            self.assertEqual(rook.__class__, Rook)
        black_rooks = [board[(0, 7)], board[(7, 7)]]
        for rook in black_rooks:
            self.assertEqual(rook.color, 'black')
            self.assertEqual(rook.__class__, Rook)
        # Knight
        white_knights = [board[(1, 0)], board[(6, 0)]]
        for knight in white_knights:
            self.assertEqual(knight.color, 'white')
            self.assertEqual(knight.__class__, Knight)
        black_knights = [board[(1, 7)], board[(6, 7)]]
        for knight in black_knights:
            self.assertEqual(knight.color, 'black')
            self.assertEqual(knight.__class__, Knight)
        # Bishop
        white_bishops = [board[(2, 0)], board[(5, 0)]]
        for bishop in white_bishops:
            self.assertEqual(bishop.color, 'white')
            self.assertEqual(bishop.__class__, Bishop)
        black_bishops = [board[(2, 7)], board[(5, 7)]]
        for bishop in black_bishops:
            self.assertEqual(bishop.color, 'black')
            self.assertEqual(bishop.__class__, Bishop)
        # Queen
        white_queen = board[(3, 0)]
        self.assertEqual(white_queen.color, 'white')
        self.assertEqual(white_queen.__class__, Queen)
        black_queen = board[(3, 7)]
        self.assertEqual(black_queen.color, 'black')
        self.assertEqual(black_queen.__class__, Queen)
        # King
        white_king = board[(4, 0)]
        self.assertEqual(white_king.color, 'white')
        self.assertEqual(white_king.__class__, King)
        black_king = board[(4, 7)]
        self.assertEqual(black_king.color, 'black')
        self.assertEqual(black_king.__class__, King)


class TestBoard(TestBoardValid, TestBoardGetItem, TestBoardNewGame):
    pass