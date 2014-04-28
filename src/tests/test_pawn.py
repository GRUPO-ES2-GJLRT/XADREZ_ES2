# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


import unittest

from consts.colors import WHITE, BLACK
from consts.moves import (
    LEFT_EN_PASSANT, RIGHT_EN_PASSANT, PROMOTION, to_move_dict
)
from game_elements.board import Board
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.king import King


class TestPawnMove(unittest.TestCase):

    def test_white_pawn_at_4_4_can_move_to_4_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        possible_moves = to_move_dict([(4, 5)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_4_can_move_to_4_3(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 4)
        possible_moves = to_move_dict([(4, 3)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_0_1_can_move_to_0_2_and_0_3(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 0, 1)
        possible_moves = to_move_dict([(0, 2), (0, 3)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_0_6_can_move_to_0_5_and_0_4(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 0, 6)
        possible_moves = to_move_dict([(0, 5), (0, 4)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_0_1_with_piece_in_0_3_can_move_to_0_2(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 0, 1)
        Pawn(board, WHITE, 0, 3)
        possible_moves = to_move_dict([(0, 2)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_0_6_with_piece_in_0_4_can_move_to_0_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 0, 6)
        Pawn(board, WHITE, 0, 4)
        possible_moves = to_move_dict([(0, 5)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_0_1_with_piece_in_0_2_doesnt_have_any_moves(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 0, 1)
        Pawn(board, WHITE, 0, 2)
        possible_moves = to_move_dict([])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_0_6_with_piece_in_0_5_doesnt_have_any_moves(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 0, 6)
        Pawn(board, WHITE, 0, 5)
        possible_moves = to_move_dict([])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_4_4_with_enemy_at_5_5_can_move_to_4_5_and_5_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        Pawn(board, BLACK, 5, 5)
        possible_moves = to_move_dict([(4, 5)])
        attack = to_move_dict([(5, 5)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_4_4_with_enemy_at_3_5_can_move_to_4_5_and_3_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        Pawn(board, BLACK, 3, 5)
        possible_moves = to_move_dict([(4, 5)])
        attack = to_move_dict([(3, 5)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_4_with_enemy_at_3_3_can_move_to_4_3_and_3_3(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 4)
        Pawn(board, WHITE, 3, 3)
        possible_moves = to_move_dict([(4, 3)])
        attack = to_move_dict([(3, 3)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_4_with_enemy_at_5_3_can_move_to_4_3_and_5_3(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 4)
        Pawn(board, WHITE, 5, 3)
        possible_moves = to_move_dict([(4, 3)])
        attack = to_move_dict([(5, 3)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))


class TestPawnEnPassant(unittest.TestCase):

    def test_white_pawn_at_4_4_en_passant_with_enemy_at_5_4_can_move_to_4_5_and_5_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        Pawn(board, BLACK, 5, 4)
        board.last_move = (BLACK, (5, 6), (5, 4))
        possible_moves = to_move_dict([(4, 5)])
        attack = to_move_dict([(5, 5, RIGHT_EN_PASSANT)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_4_4_en_passant_with_enemy_at_3_4_can_move_to_4_5_and_3_5(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 4)
        Pawn(board, BLACK, 3, 4)
        board.last_move = (BLACK, (3, 6), (3, 4))
        possible_moves = to_move_dict([(4, 5)])
        attack = to_move_dict([(3, 5, LEFT_EN_PASSANT)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_3_en_passant_with_enemy_at_3_3_can_move_to_4_2_and_3_2(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 3)
        Pawn(board, WHITE, 3, 3)
        board.last_move = (WHITE, (3, 1), (3, 3))
        possible_moves = to_move_dict([(4, 2)])
        attack = to_move_dict([(3, 2, LEFT_EN_PASSANT)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_3_en_passant_with_enemy_at_5_3_can_move_to_4_2_and_5_2(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 3)
        Pawn(board, WHITE, 5, 3)
        board.last_move = (WHITE, (5, 1), (5, 3))
        possible_moves = to_move_dict([(4, 2)])
        attack = to_move_dict([(5, 2, RIGHT_EN_PASSANT)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))


class TestPawnAttackMoves(unittest.TestCase):

    def test_black_pawn_at_4_3_if_hindered_false_shows_attack_position_even_if_there_is_no_enemy(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 3)
        attack = to_move_dict([(3, 2), (5, 2)])

        self.assertEqual(pawn.attack_moves(), attack)

    def test_black_pawn_at_4_3_ignores_en_passant_if_hindered_false_with_enemy_at_5_3(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 3)
        Pawn(board, WHITE, 5, 3)
        board.last_move = (WHITE, (5, 1), (5, 3))
        attack = to_move_dict([(3, 2), (5, 2)])

        self.assertEqual(pawn.attack_moves(), attack)


class TestPawnPromotion(unittest.TestCase):

    def test_white_pawn_at_4_6_should_be_promoted_at_4_7(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 6)
        possible_moves = to_move_dict([(4, 7, PROMOTION)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_white_pawn_at_4_6_with_enemy_at_5_7_should_be_promoted_at_5_7(self):
        board = Board(new_game=False)
        pawn = Pawn(board, WHITE, 4, 6)
        Pawn(board, BLACK, 5, 7)
        possible_moves = to_move_dict([(4, 7, PROMOTION)])
        attack = to_move_dict([(5, 7, PROMOTION)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_1_should_be_promoted_at_4_0(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 1)
        possible_moves = to_move_dict([(4, 0, PROMOTION)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_black_pawn_at_4_1_with_enemy_at_5_0_should_be_promoted_at_5_0(self):
        board = Board(new_game=False)
        pawn = Pawn(board, BLACK, 4, 1)
        Pawn(board, WHITE, 5, 0)
        possible_moves = to_move_dict([(4, 0, PROMOTION)])
        attack = to_move_dict([(5, 0, PROMOTION)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))


class TestPawnProtectsKing(unittest.TestCase):

    def test_pawn_can_move_if_it_doesnt_protect_the_king(self):
        board = Board(new_game=False)
        King(board, WHITE, 3, 1)
        pawn = Pawn(board, WHITE, 4, 4)
        possible_moves = to_move_dict([(4, 5)])
        attack = {}

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_pawn_can_move_to_protect_the_king(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 2)
        pawn = Pawn(board, WHITE, 3, 1)
        Queen(board, BLACK, 2, 2)
        possible_moves = to_move_dict([(3, 2)])
        attack = to_move_dict([(2, 2)])

        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))

    def test_pawn_cannot_move_if_it_is_protecting_the_king(self):
        board = Board(new_game=False)
        King(board, WHITE, 4, 1)
        Queen(board, BLACK, 0, 1)
        pawn = Pawn(board, WHITE, 3, 1)
        possible_moves = {}
        attack = {}
        self.assertEqual(pawn.possible_moves(), (possible_moves, attack))


class TestPawn(TestPawnMove, TestPawnEnPassant, TestPawnAttackMoves,
               TestPawnPromotion, TestPawnProtectsKing):
    pass
