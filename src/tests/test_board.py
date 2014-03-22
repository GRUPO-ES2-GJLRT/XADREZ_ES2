# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from consts.colors import WHITE, BLACK
from consts.moves import CHECK, CHECKMATE, STALEMATE, NORMAL, FIFTY_MOVE

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


class TestBoardMoves(unittest.TestCase):

    def test_moves_in_a_board_with_just_a_knight(self):
        board = Board(new_game=False)
        knight = Knight(board, WHITE, 4, 4)
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
        self.assertEqual(set(board.possible_moves(WHITE).keys()), expected_moves_white)
        self.assertEqual(set(board.possible_moves(BLACK).keys()), expected_moves_black)

    def test_moves_in_a_new_game(self):
        board = Board(new_game=True)
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
        self.assertEqual(set(board.possible_moves(WHITE).keys()), expected_moves_white)
        self.assertEqual(set(board.possible_moves(BLACK).keys()), expected_moves_black)

    def test_moves_that_allows_check_are_not_allowed(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 0)
        Pawn(board, WHITE, 5, 1)
        Bishop(board, BLACK, 7, 3)
        expected_moves_white = set([
            ((4, 0), (3, 0)), 
            ((4, 0), (3, 1)),
            ((4, 0), (5, 0)),
            ((4, 0), (4, 1)),
               
        ])
        self.assertEqual(set(board.possible_moves(WHITE).keys()), expected_moves_white)


    def test_moves_that_keeps_check_are_not_allowed(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 0)
        Pawn(board, WHITE, 4, 1)
        Rook(board, BLACK, 0, 0)
        expected_moves_white = set([
            ((4, 0), (3, 1)),
            ((4, 0), (5, 1)),
        ])
        self.assertEqual(set(board.possible_moves(WHITE).keys()), expected_moves_white)


class TestBoardInCheck(unittest.TestCase):

    def test_king_is_in_check_if_it_is_hindered(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 4, 4)
        king = King(board, BLACK, 4, 7)
        board.current_color = BLACK
        self.assertEqual(board.in_check(), True)

    def test_king_is_not_in_check_if_it_is_not_hindered(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 7)
        board.current_color = BLACK
        self.assertEqual(board.in_check(), False)

    def test_king_is_in_check_custom_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        board.current_color = BLACK
        self.assertEqual(board.in_check(hindered=set([(4,7)])), True)

    def test_king_is_not_in_check_custom_hindered(self):
        board = Board(new_game=False)
        king = King(board, BLACK, 4, 7)
        board.current_color = BLACK
        self.assertEqual(board.in_check(hindered=set()), False)
        
        
class TestBoardInCheckmate(unittest.TestCase):

    def test_king_is_in_checkmate(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 4)
        Rook(board, WHITE, 3, 4)
        Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 7)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.in_checkmate(), True)

    def test_king_is_in_checkmate2(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 4)
        Rook(board, WHITE, 3, 4)
        Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 6)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.in_checkmate(), True)

    def test_king_is_not_in_checkmate(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 6)
        Rook(board, WHITE, 0, 7)
        king = King(board, BLACK, 4, 7)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.in_checkmate(), False)

    def test_king_is_not_in_checkmate(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 0)
        king = King(board, BLACK, 4, 7)
        Bishop(board, BLACK, 3, 7)
        Bishop(board, BLACK, 5, 7)
        Pawn(board, BLACK, 3, 6)
        Pawn(board, BLACK, 5, 6)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.in_checkmate(), False)

    def test_king_is_not_in_checkmate_custom_hindered(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 4)
        Rook(board, WHITE, 3, 4)
        Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 7)
        king.ignored = True
        hindered = set([(3, 6), (3, 7), (4, 6), (5, 6), (5, 7)])
        board.current_color = BLACK
        self.assertEqual(board.in_checkmate(hindered=hindered), False)


class TestBoardStalemate(unittest.TestCase):

    def test_stalemate(self):
        board = Board(new_game=False)
        King(board, WHITE, 5, 6)
        Queen(board, WHITE, 6, 5)
        king = King(board, BLACK, 7, 7)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.stalemate(), True)

    def test_stalemate_false(self):
        board = Board(new_game=False)
        King(board, WHITE, 5, 6)
        king = King(board, BLACK, 7, 7)
        king.ignored = True
        board.current_color = BLACK
        self.assertEqual(board.stalemate(), False)

    def test_stalemate_false_custom_hindered(self):
        board = Board(new_game=False)
        King(board, WHITE, 5, 6)
        Queen(board, WHITE, 6, 5)
        king = King(board, BLACK, 7, 7)
        king.ignored = True
        hindered = set([(7, 6), (6, 6), (6, 7), (7, 7)])
        board.current_color = BLACK
        self.assertEqual(board.stalemate(hindered=hindered), False)


class TestBoardStatus(unittest.TestCase):

    def test_check_status(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 4, 4)
        king = King(board, BLACK, 4, 7)
        board.current_color = BLACK
        self.assertEqual(board.status(), CHECK)

    def test_checkmate_status(self):
        board = Board(new_game=False)
        Rook(board, WHITE, 4, 4)
        Rook(board, WHITE, 3, 4)
        Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 6)
        board.current_color = BLACK
        self.assertEqual(board.status(), CHECKMATE)
        
    def test_stalemate_status(self):
        board = Board(new_game=False)
        King(board, WHITE, 5, 6)
        Queen(board, WHITE, 6, 5)
        King(board, BLACK, 7, 7)
        board.current_color = BLACK
        self.assertEqual(board.status(), STALEMATE)

    def test_fifty_move_status(self):
        board = Board(new_game=False)
        King(board, BLACK, 7, 7)
        board.moves[BLACK] = 50
        board.current_color = BLACK
        self.assertEqual(board.status(), FIFTY_MOVE)

    def test_normal_status(self):
        board = Board(new_game=False)
        King(board, BLACK, 7, 7)
        board.current_color = BLACK
        self.assertEqual(board.status(), NORMAL)
        

class TestBoardMove(unittest.TestCase):

    def test_invalid_original_position(self):
        board = Board(new_game=False)
        self.assertEqual(False, board.move((-1, 0), (0, 0)))

    def test_invalid_new_position(self):
        board = Board(new_game=False)
        King(board, WHITE, 0, 0)
        self.assertEqual(False, board.move((0, 0), (-1, 0)))

    def test_no_piece_on_original_position(self):
        board = Board(new_game=False)
        self.assertEqual(False, board.move((0, 0), (1, 0)))
        
    def test_invalid_equal_position(self):
        board = Board(new_game=False)
        King(board, WHITE, 0, 0)
        self.assertEqual(False, board.move((0, 0), (0, 0)))

    def test_invalid_move(self):
        board = Board(new_game=False)
        King(board, WHITE, 0, 0)
        self.assertEqual(False, board.move((0, 0), (0, 2)))

    def test_invalid_color(self):
        board = Board(new_game=False)
        board.current_color = BLACK
        King(board, WHITE, 0, 0)
        self.assertEqual(False, board.move((0, 0), (0, 1)))

    def test_normal_move(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        self.assertEqual(board[(4, 0)], king)
        self.assertEqual(king.y, 0)
        self.assertEqual(True, board.move((4, 0), (4, 1)))
        self.assertEqual(True, king.has_moved)
        self.assertEqual(board[(4, 0)], None)
        self.assertEqual(board[(4, 1)], king)
        self.assertEqual(king.y, 1)
        
    def test_normal_attack_move(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        pawn = Pawn(board, BLACK, 4, 1)
        self.assertEqual(board[(4, 0)], king)
        self.assertEqual(board[(4, 1)], pawn)
        self.assertEqual(board.pieces[WHITE], [king])
        self.assertEqual(board.pieces[BLACK], [pawn])
        self.assertEqual(king.y, 0)

        self.assertEqual(True, board.move((4, 0), (4, 1)))
        self.assertEqual(True, king.has_moved)
        
        self.assertEqual(board[(4, 0)], None)
        self.assertEqual(board[(4, 1)], king)
        self.assertEqual(king.y, 1)
        self.assertEqual(board.pieces[WHITE], [king])
        self.assertEqual(board.pieces[BLACK], [])

    def test_queenside_castling_move(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        rook = Rook(board, WHITE, 0, 0)
        self.assertEqual(board[(4, 0)], king)
        self.assertEqual(board[(0, 0)], rook)
        self.assertEqual(board.pieces[WHITE], [king, rook])
        self.assertEqual(king.x, 4)
        self.assertEqual(rook.x, 0)

        self.assertEqual(True, board.move((4, 0), (2, 0)))
        self.assertEqual(True, king.has_moved)
        self.assertEqual(True, rook.has_moved)
        
        self.assertEqual(board[(4, 0)], None)
        self.assertEqual(board[(0, 0)], None)
        self.assertEqual(board[(2, 0)], king)
        self.assertEqual(board[(3, 0)], rook)
        
        self.assertEqual(board.pieces[WHITE], [king, rook])
        self.assertEqual(king.x, 2)
        self.assertEqual(rook.x, 3)
    
    def test_kingside_castling_move(self):
        board = Board(new_game=False)
        board.current_color = BLACK
        king = King(board, BLACK, 4, 7)
        rook = Rook(board, BLACK, 7, 7)
        self.assertEqual(board[(4, 7)], king)
        self.assertEqual(board[(7, 7)], rook)
        self.assertEqual(board.pieces[BLACK], [king, rook])
        self.assertEqual(king.x, 4)
        self.assertEqual(rook.x, 7)

        self.assertEqual(True, board.move((4, 7), (6, 7)))
        self.assertEqual(True, king.has_moved)
        self.assertEqual(True, rook.has_moved)
        
        self.assertEqual(board[(4, 7)], None)
        self.assertEqual(board[(7, 7)], None)
        self.assertEqual(board[(6, 7)], king)
        self.assertEqual(board[(5, 7)], rook)
        
        self.assertEqual(board.pieces[BLACK], [king, rook])
        self.assertEqual(king.x, 6)
        self.assertEqual(rook.x, 5)

    def test_right_en_passant_move(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        enemy = Pawn(board, BLACK, 5, 6)
        board.current_color = BLACK
        self.assertEqual(True, board.move((5, 6), (5, 4)))
        
        self.assertEqual(board[(4, 4)], pawn)
        self.assertEqual(board[(5, 4)], enemy)
        self.assertEqual(board.pieces[WHITE], [pawn])
        self.assertEqual(board.pieces[BLACK], [enemy])
        self.assertEqual(pawn.position, (4, 4))
        
        self.assertEqual(True, board.move((4, 4), (5, 5)))
        self.assertEqual(True, pawn.has_moved)
        
        self.assertEqual(board[(4, 4)], None)
        self.assertEqual(board[(5, 5)], pawn)
        self.assertEqual(board[(5, 4)], None)
        
        self.assertEqual(board.pieces[WHITE], [pawn])
        self.assertEqual(board.pieces[BLACK], [])
        self.assertEqual(pawn.position, (5, 5))

    def test_left_en_passant_move(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        enemy = Pawn(board, BLACK, 3, 6)
        board.current_color = BLACK
        self.assertEqual(True, board.move((3, 6), (3, 4)))
        
        self.assertEqual(board[(4, 4)], pawn)
        self.assertEqual(board[(3, 4)], enemy)
        self.assertEqual(board.pieces[WHITE], [pawn])
        self.assertEqual(board.pieces[BLACK], [enemy])
        self.assertEqual(pawn.position, (4, 4))
        
        self.assertEqual(True, board.move((4, 4), (3, 5)))
        self.assertEqual(True, pawn.has_moved)
        
        self.assertEqual(board[(4, 4)], None)
        self.assertEqual(board[(3, 5)], pawn)
        self.assertEqual(board[(3, 4)], None)
        
        self.assertEqual(board.pieces[WHITE], [pawn])
        self.assertEqual(board.pieces[BLACK], [])
        self.assertEqual(pawn.position, (3, 5))

    def test_promotion_move(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 6)

        self.assertEqual(board[(4, 6)], pawn)
        self.assertEqual(board.pieces[WHITE], [pawn])
        self.assertEqual(pawn.position, (4, 6))
        
        self.assertEqual(True, board.move((4, 6), (4, 7)))
        
        # ToDo: verificar. Vai ser sempre rainha?
        self.assertEqual(board[(4, 7)].__class__, Queen)
        self.assertEqual(board[(4, 6)], None)
        self.assertEqual(True, board[(4, 7)].has_moved)
        
        self.assertEqual(board.pieces[WHITE], [board[(4, 7)]])
        
    def test_invalid_keep_check(self):
        board = Board(new_game=False)
        king = King(board, WHITE, 4, 0)
        Pawn(board, WHITE, 4, 1)
        Rook(board, BLACK, 0, 0)
        Rook(board, BLACK, 5, 0)
        board.current_color = WHITE
        self.assertEqual(False, king.has_moved)
        self.assertEqual(False, board.move((4, 0), (5, 0)))
        
        self.assertEqual(False, king.has_moved)
        
        self.assertEqual(board[(4, 0)], king)
        self.assertEqual(board[(5, 0)].__class__, Rook)
        self.assertEqual(king.position, (4, 0))

    def test_check(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 5, 4)
        king = King(board, BLACK, 4, 7)
        board.current_color = WHITE

        self.assertEqual(False, rook.has_moved)
        self.assertEqual(True, board.move((5, 4), (4, 4)))
        self.assertEqual(True, rook.has_moved)
        
        self.assertEqual(board[(5, 4)], None)
        self.assertEqual(board[(4, 4)], rook)
        self.assertEqual(rook.position, (4, 4))

    def test_checkmate(self):
        board = Board(new_game=False)
        rook = Rook(board, WHITE, 5, 4)
        Rook(board, WHITE, 5, 0)
        Rook(board, WHITE, 3, 0)

        king = King(board, BLACK, 4, 7)
        board.current_color = WHITE

        self.assertEqual(False, rook.has_moved)
        self.assertEqual(True, board.move((5, 4), (4, 4)))
        self.assertEqual(True, rook.has_moved)
        
        self.assertEqual(board[(5, 4)], None)
        self.assertEqual(board[(4, 4)], rook)
        self.assertEqual(rook.position, (4, 4))


class TestBoard(TestBoardValid, TestBoardGetItem, TestBoardNewGame, 
    TestBoardRemove, TestBoardHindered, TestBoardMoves, TestBoardInCheck, 
    TestBoardInCheckmate, TestBoardStalemate, TestBoardStatus, TestBoardMove):
    pass