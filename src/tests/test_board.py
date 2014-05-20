# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


import unittest

from consts.colors import WHITE, BLACK
from consts.moves import CHECK, CHECKMATE, STALEMATE, NORMAL, FIFTY_MOVE
from cython.importer import Board

tuples = lambda x: set(a.tuple() for a in x)

BP, WP = "black pawn", "white pawn"
BR, WR = "black rook", "white rook"
BN, WN = "black knight", "white knight"
BB, WB = "black bishop", "white bishop"
BQ, WQ = "black queen", "white queen"
BK, WK = "black king", "white king"


class TestBoardAt(unittest.TestCase):

    def test_get_from_valid_position_without_piece_returns_none(self):
        board = Board(False)
        self.assertEqual(board.at((4, 4)), None)

    def test_get_from_valid_position_with_piece_returns_piece(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
        self.assertEqual(board.at((4, 4)), WN)

    def test_get_from_invalid_position_returns_none(self):
        board = Board(False)
        self.assertEqual(board.at((-4, 4)), None)

    def test_current_king_position_white(self):
        board = Board(True)
        self.assertEqual(board.current_king_position(), (4, 0))

    def test_current_king_position_black(self):
        board = Board(True)
        board.load_fen(
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual(board.current_king_position(), (4, 7))




class TestBoardNewGame(unittest.TestCase):

    def test_create_board_new_game_false(self):
        board = Board(False)
        for x in xrange(8):
            for y in xrange(8):
                self.assertEqual(board.at((x, y)), None)

    def test_create_board_new_game_true(self):
        board = Board(True)
        # Pawn
        for x in xrange(8):
            self.assertEqual(board.at((x, 6)), BP)
            self.assertEqual(board.at((x, 1)), WP)

        # Rook
        self.assertEqual(board.at((0, 0)), WR)
        self.assertEqual(board.at((7, 0)), WR)
        self.assertEqual(board.at((0, 7)), BR)
        self.assertEqual(board.at((7, 7)), BR)

        # Knight
        self.assertEqual(board.at((1, 0)), WN)
        self.assertEqual(board.at((6, 0)), WN)
        self.assertEqual(board.at((1, 7)), BN)
        self.assertEqual(board.at((6, 7)), BN)

        # Bishop
        self.assertEqual(board.at((2, 0)), WB)
        self.assertEqual(board.at((5, 0)), WB)
        self.assertEqual(board.at((2, 7)), BB)
        self.assertEqual(board.at((5, 7)), BB)

        # Queen
        self.assertEqual(board.at((3, 0)), WQ)
        self.assertEqual(board.at((3, 7)), BQ)

        # King
        self.assertEqual(board.at((4, 0)), WK)
        self.assertEqual(board.at((4, 7)), BK)


class TestBoardHindered(unittest.TestCase):

    def test_hindered_in_a_board_with_just_a_knight(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
        expected_hindered_white = set([
            (3, 2), (5, 2), (6, 3), (6, 5), (5, 6), (3, 6), (2, 5), (2, 3)
        ])
        expected_hindered_black = set()
        self.assertEqual(board.hindered(WHITE), expected_hindered_white)
        self.assertEqual(board.hindered(BLACK), expected_hindered_black)
        self.assertEqual(board.hindered(-1), expected_hindered_white)

    def test_hindered_in_a_new_game(self):
        board = Board(True)
        expected_hindered_white = set([
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)
        ])
        expected_hindered_black = set([
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)
        ])
        self.assertEqual(board.hindered(WHITE), expected_hindered_white)
        self.assertEqual(board.hindered(BLACK), expected_hindered_black)
        self.assertEqual(board.hindered(-1), expected_hindered_white)


class TestBoardMoves(unittest.TestCase):

    def test_moves_in_a_board_with_just_a_knight(self):
        board = Board(False)
        board.load_fen("8/8/8/4N3/8/8/8/8 w kQkq - 0 1")
        expected_moves_white = set([
            ((4, 4), (3, 2)),
            ((4, 4), (5, 2)),
            ((4, 4), (6, 3)),
            ((4, 4), (6, 5)),
            ((4, 4), (5, 6)),
            ((4, 4), (3, 6)),
            ((4, 4), (2, 5)),
            ((4, 4), (2, 3)),
        ])
        expected_moves_black = set()
        self.assertEqual(tuples(board.possible_moves(WHITE)),
                         expected_moves_white)
        self.assertEqual(tuples(board.possible_moves(BLACK)),
                         expected_moves_black)

    def test_moves_in_a_new_game(self):
        board = Board(True)
        expected_moves_white = set([
            ((0, 1), (0, 2)), ((0, 1), (0, 3)),
            ((1, 1), (1, 2)), ((1, 1), (1, 3)),
            ((2, 1), (2, 2)), ((2, 1), (2, 3)),
            ((3, 1), (3, 2)), ((3, 1), (3, 3)),
            ((4, 1), (4, 2)), ((4, 1), (4, 3)),
            ((5, 1), (5, 2)), ((5, 1), (5, 3)),
            ((6, 1), (6, 2)), ((6, 1), (6, 3)),
            ((7, 1), (7, 2)), ((7, 1), (7, 3)),
            ((1, 0), (0, 2)), ((1, 0), (2, 2)),
            ((6, 0), (5, 2)), ((6, 0), (7, 2)),
        ])
        expected_moves_black = set([
            ((0, 6), (0, 5)), ((0, 6), (0, 4)),
            ((1, 6), (1, 5)), ((1, 6), (1, 4)),
            ((2, 6), (2, 5)), ((2, 6), (2, 4)),
            ((3, 6), (3, 5)), ((3, 6), (3, 4)),
            ((4, 6), (4, 5)), ((4, 6), (4, 4)),
            ((5, 6), (5, 5)), ((5, 6), (5, 4)),
            ((6, 6), (6, 5)), ((6, 6), (6, 4)),
            ((7, 6), (7, 5)), ((7, 6), (7, 4)),
            ((1, 7), (0, 5)), ((1, 7), (2, 5)),
            ((6, 7), (5, 5)), ((6, 7), (7, 5)),
        ])
        self.assertEqual(tuples(board.possible_moves(WHITE)),
                         expected_moves_white)
        self.assertEqual(tuples(board.possible_moves(BLACK)),
                         expected_moves_black)

    def test_moves_that_allows_check_are_not_allowed(self):
        board = Board(False)
        board.load_fen("8/8/8/8/7b/8/5P2/4K3 w - - 0 1")
        expected_moves_white = set([
            ((4, 0), (3, 0)),
            ((4, 0), (3, 1)),
            ((4, 0), (5, 0)),
            ((4, 0), (4, 1)),

        ])
        self.assertEqual(tuples(board.possible_moves(WHITE)),
                         expected_moves_white)

    def test_moves_that_keeps_check_are_not_allowed(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/4P3/r3K3 w kQkq - 0 1")
        expected_moves_white = set([
            ((4, 0), (3, 1)),
            ((4, 0), (5, 1)),
        ])
        self.assertEqual(tuples(board.possible_moves(WHITE)),
                         expected_moves_white)



class TestKillingMoves(unittest.TestCase):
    
    def test_capture_killing_moves(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/2p5/3P3P/8 w kQkq - 0 1")
        expected_moves_white = set([
            ((3, 1), (2, 2)),
        ])
        expected_moves_black = set([
            ((2, 2), (3, 1)),
        ])
        self.assertEqual(tuples(board.possible_killing_moves(WHITE)),
                         expected_moves_white)
        self.assertEqual(tuples(board.possible_killing_moves(BLACK)),
                         expected_moves_black)

    def test_en_passant_killing_moves(self):
        board = Board(False)
        board.load_fen("8/8/8/8/2pP4/8/7P/8 b kQkq d3 0 1")
        expected_moves_white = set()
        expected_moves_black = set([
            ((2, 3), (3, 2)),
        ])
        self.assertEqual(tuples(board.possible_killing_moves(WHITE)),
                         expected_moves_white)
        self.assertEqual(tuples(board.possible_killing_moves(BLACK)),
                         expected_moves_black)


    def test_piece_attack_moves(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/p7/8/R3P3 b kQkq d3 0 1")
        expected_moves_white = set([
            ((0, 0), (0, 1)), ((0, 0), (0, 2)), 
            ((0, 0), (1, 0)), ((0, 0), (2, 0)), ((0, 0), (3, 0)),
        ])
        self.assertEqual(tuples(board.piece_attack_moves((0, 0))),
                         expected_moves_white)


class TestBoardStatus(unittest.TestCase):

    def test_check_status(self):
        board = Board(False)
        board.load_fen("4k3/8/8/4R3/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(board.status(None), CHECK)

    def test_checkmate_status(self):
        board = Board(False)
        board.load_fen("8/4k3/8/3RRR2/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(board.status(None), CHECKMATE)

    def test_stalemate_status(self):
        board = Board(False)
        board.load_fen("7k/5K2/6Q1/8/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(board.status(None), STALEMATE)

    def test_fifty_move_status(self):
        board = Board(False)
        board.load_fen("7k/8/8/8/8/8/8/8 b kQkq - 50 50")
        self.assertEqual(board.status(None), FIFTY_MOVE)

    def test_normal_status(self):
        board = Board(False)
        board.load_fen("7k/8/8/8/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(board.status(None), NORMAL)


class TestBoardMove(unittest.TestCase):

    def test_invalid_original_position(self):
        board = Board(False)
        self.assertEqual(False, board.move((-1, 0), (0, 0)))

    def test_invalid_new_position(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/K7 w kQkq - 0 1")
        self.assertEqual(False, board.move((0, 0), (-1, 0)))

    def test_no_piece_on_original_position(self):
        board = Board(False)
        self.assertEqual(False, board.move((0, 0), (1, 0)))

    def test_invalid_equal_position(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/K7 w kQkq - 0 1")
        self.assertEqual(False, board.move((0, 0), (0, 0)))

    def test_invalid_move(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/K7 w kQkq - 0 1")
        self.assertEqual(False, board.move((0, 0), (0, 2)))

    def test_invalid_color(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/K7 b kQkq - 0 1")
        self.assertEqual(False, board.move((0, 0), (0, 1)))

    def test_normal_move(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/4K3 w kQkq - 0 1")
        self.assertEqual(board.at((4, 0)), WK)
        self.assertEqual(True, board.move((4, 0), (4, 1)))
        self.assertEqual(board.at((4, 0)), None)
        self.assertEqual(board.at((4, 1)), WK)

    def test_normal_attack_move(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/4p3/4K3 w kQkq - 0 1")
        self.assertEqual(board.at((4, 0)), WK)
        self.assertEqual(board.at((4, 1)), BP)
        self.assertEqual(True, board.move((4, 0), (4, 1)))
        self.assertEqual(board.at((4, 0)), None)
        self.assertEqual(board.at((4, 1)), WK)

    def test_queenside_castling_move(self):
        board = Board(False)
        board.load_fen("8/8/8/8/8/8/8/R3K3 w kQkq - 0 1")
        self.assertEqual(board.at((4, 0)), WK)
        self.assertEqual(board.at((0, 0)), WR)
        self.assertEqual(True, board.move((4, 0), (2, 0)))
        self.assertEqual(board.at((4, 0)), None)
        self.assertEqual(board.at((0, 0)), None)
        self.assertEqual(board.at((2, 0)), WK)
        self.assertEqual(board.at((3, 0)), WR)

    def test_kingside_castling_move(self):
        board = Board(False)
        board.load_fen("4k2r/8/8/8/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(board.at((4, 7)), BK)
        self.assertEqual(board.at((7, 7)), BR)
        self.assertEqual(True, board.move((4, 7), (6, 7)))
        self.assertEqual(board.at((4, 7)), None)
        self.assertEqual(board.at((7, 7)), None)
        self.assertEqual(board.at((6, 7)), BK)
        self.assertEqual(board.at((5, 7)), BR)

    def test_right_en_passant_move(self):
        board = Board(False)
        board.load_fen("8/5p2/8/4P3/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(True, board.move((5, 6), (5, 4)))
        self.assertEqual(board.at((4, 4)), WP)
        self.assertEqual(board.at((5, 4)), BP)
        self.assertEqual(True, board.move((4, 4), (5, 5)))
        self.assertEqual(board.at((4, 4)), None)
        self.assertEqual(board.at((5, 5)), WP)
        self.assertEqual(board.at((5, 4)), None)

    def test_left_en_passant_move(self):
        board = Board(False)
        board.load_fen("8/3p4/8/4P3/8/8/8/8 b kQkq - 0 1")
        self.assertEqual(True, board.move((3, 6), (3, 4)))
        self.assertEqual(board.at((4, 4)), WP)
        self.assertEqual(board.at((3, 4)), BP)
        self.assertEqual(True, board.move((4, 4), (3, 5)))
        self.assertEqual(board.at((4, 4)), None)
        self.assertEqual(board.at((3, 5)), WP)
        self.assertEqual(board.at((3, 4)), None)

    def test_promotion_move(self):
        board = Board(False)
        board.load_fen("8/4P3/8/8/8/8/8/8 w kQkq - 0 1")
        self.assertEqual(board.at((4, 6)), WP)
        self.assertEqual(True, board.move((4, 6), (4, 7)))
        # ToDo: verificar. Vai ser sempre rainha?
        self.assertEqual(board.at((4, 7)), WQ)
        self.assertEqual(board.at((4, 6)), None)

    def test_invalid_keep_check(self):
        board = Board(False)
        board.load_fen("8/4P3/8/8/8/8/4P3/r3Kr2 w kQkq - 0 1")
        self.assertEqual(False, board.move((4, 0), (5, 0)))
        self.assertEqual(board.at((4, 0)), WK)
        self.assertEqual(board.at((5, 0)), BR)

    def test_check(self):
        board = Board(False)
        board.load_fen("4k3/8/8/5R2/8/8/8/8 w kQkq - 0 1")
        self.assertEqual(True, board.move((5, 4), (4, 4)))
        self.assertEqual(board.at((5, 4)), None)
        self.assertEqual(board.at((4, 4)), WR)

    def test_checkmate(self):
        board = Board(False)
        board.load_fen("4k3/8/8/5R2/8/8/8/3R1R2 w kQkq - 0 1")
        self.assertEqual(True, board.move((5, 4), (4, 4)))
        self.assertEqual(board.at((5, 4)), None)
        self.assertEqual(board.at((4, 4)), WR)


class TestClone(unittest.TestCase):

    def test_clone_board(self):
        board = Board(False)
        board.load_fen("4k3/8/8/5R2/8/8/8/3R1R2 w kQkq - 0 1")
        clone = board.clone()
        self.assertEqual(clone.at((5, 4)), WR)
        self.assertEqual(clone.at((4, 7)), BK)
        self.assertEqual(clone.at((3, 0)), WR)
        self.assertEqual(clone.at((5, 0)), WR)
        self.assertEqual(clone.color(), board.color())
        self.assertEqual(clone.get_hash(), board.get_hash())


class TestPieces(unittest.TestCase):

    def test_get_pieces(self):
        board = Board(False)
        board.load_fen("8/8/8/5R2/5p2/8/8/8 w kQkq - 0 1")
        pieces = board.get_pieces()
        self.assertEqual(pieces[0].name, "rook")
        self.assertEqual(pieces[0].color, "white")
        self.assertEqual(pieces[0].position, (5, 4))
        self.assertEqual(pieces[1].name, "pawn")
        self.assertEqual(pieces[1].color, "black")
        self.assertEqual(pieces[1].position, (5, 3))


class TestBoard(TestBoardAt,
                TestBoardNewGame,
                TestBoardHindered,
                TestBoardMoves,
                TestKillingMoves,
                TestBoardStatus,
                TestBoardMove,
                TestClone,
                TestPieces):
    pass
