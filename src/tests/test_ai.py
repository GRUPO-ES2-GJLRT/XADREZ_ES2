# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from cython.functions import (
    p0x88_to_tuple,
    tuple_to_0x88,
    chess_notation_to_0x88,
    p0x88_to_chess_notation,
    chess_notation_to_tuple
)

from cython.importer import Board
from consts.colors import WHITE, BLACK
from consts.pieces import PAWN, KING


class TestBoardEvaluation(unittest.TestCase):

    def test_initial_get_value(self):
        board = Board(True)
        self.assertEqual(board.get_value(), 0)


    def test_get_value_when_white_is_winning(self):
        board = Board(False)
        board.load_fen(
            "rnbqkbnr/ppppp1pp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertGreater(board.get_value(), 0)

    def test_get_value_when_black_is_winning(self):
        board = Board(False)
        board.load_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertLess(board.get_value(), 0)


class TestBoardPiecesCount(unittest.TestCase):

    def test_white_pawns_count(self):
        board = Board(True)
        self.assertEqual(board.count(WHITE, PAWN), 8)

    def test_black_pawns_count(self):
        board = Board(True)
        self.assertEqual(board.count(BLACK, PAWN), 8)

    def test_white_king_count(self):
        board = Board(True)
        self.assertEqual(board.count(WHITE, KING), 1)

    def test_black_king_count(self):
        board = Board(True)
        self.assertEqual(board.count(BLACK, KING), 1)
    
   
class TestAI(TestBoardEvaluation,
             TestBoardPiecesCount):
    pass