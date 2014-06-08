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

from time import sleep
from cython.importer import Board
from consts.colors import WHITE, BLACK
from game_elements import Player, InputPlayer, AIPlayer
from game_elements.player import SELECT, PLAY, END
from game_elements.ai_player import RANDOM, SEMI_RANDOM, EASY


class MockGame(object):

    def __init__(self):
        self.running = True

class MockChess(object):

    def __init__(self):
        self.board = Board(True)
        self.winner = None
        self.selected = None
        self.played = False
        self.confirm_draw = None
        self.draw_denied = None
        self.state = None
        self.ai_timeout = 1
        self.game = MockGame()

    def win(self, color):
        self.winner = color

    def select(self, square):
        self.selected = square

    def play(self, square, promotion):
        if self.selected:
            self.played = True
        return self.played

    def confirm_draw_dialog(self, player):
        self.confirm_draw = player

    def deny_draw(self, player):
        self.draw_denied = player

    def do_jit_draw(self):
        pass


class MockTimer(object):

    def __init__(self):
        self.turn_started = False
        self.turn_end = False
        self.started = False
        self.player = None

    def start_turn(self):
        self.turn_ended = False
        self.turn_started = True

    def end_turn(self):
        self.turn_ended = True
        self.turn_started = False

    def start(self):
        self.started = True


class TestBasePlayer(unittest.TestCase):

    def test_new_player(self):
        timer = MockTimer()
        chess = MockChess()
        player = Player(WHITE, timer, chess)
        self.assertEqual(player.color, WHITE)
        self.assertEqual(player.timer, timer)
        self.assertEqual(player.chess, chess)
        self.assertEqual(player.state, None)
        self.assertEqual(timer.player, player)
        self.assertEqual(timer.started, True)

    def test_player_start_turn(self):
        timer = MockTimer()
        chess = MockChess()
        player = Player(WHITE, timer, chess)
        player.start_turn()
        self.assertEqual(player.state, SELECT)
        self.assertEqual(timer.turn_started, True)

    def test_player_end_turn(self):
        timer = MockTimer()
        chess = MockChess()
        player = Player(WHITE, timer, chess)
        player.start_turn()
        player.end_turn()
        self.assertEqual(player.state, None)
        self.assertEqual(timer.turn_ended, True)

    def test_player_pause_turn(self):
        timer = MockTimer()
        chess = MockChess()
        player = Player(WHITE, timer, chess)
        player.start_turn()
        player.pause_turn()
        self.assertEqual(player.state, SELECT)
        self.assertEqual(timer.turn_ended, True)
        self.assertEqual(timer.turn_started, False)

    def test_player_resume_turn(self):
        timer = MockTimer()
        chess = MockChess()
        player = Player(WHITE, timer, chess)
        player.start_turn()
        player.pause_turn()
        player.resume_turn()
        self.assertEqual(player.state, SELECT)
        self.assertEqual(timer.turn_ended, False)
        self.assertEqual(timer.turn_started, True)

    def test_player_lose(self):
        chess = MockChess()
        player = Player(WHITE, MockTimer(), chess)
        player.lose()
        self.assertEqual(chess.winner, BLACK)

    def test_player_select(self):
        chess = MockChess()
        player = Player(WHITE, MockTimer(), chess)
        player.select((0, 0))
        self.assertEqual(chess.selected, (0, 0))

    def test_player_play(self):
        chess = MockChess()
        player = Player(WHITE, MockTimer(), chess)
        self.assertEqual(player.play((0, 0)), False)
        self.assertEqual(chess.played, False)
        player.select((1, 1))
        self.assertEqual(player.play((1, 2)), True)
        self.assertEqual(chess.played, True)


class TestInputPlayer(unittest.TestCase):

    def test_input_player_click(self):
        timer = MockTimer()
        chess = MockChess()
        player = InputPlayer(WHITE, timer, chess)
        player.start_turn()
        player.click(False)
        self.assertEqual(chess.selected, None)
        player.click((1, 1))
        self.assertEqual(chess.selected, (1, 1))
        self.assertEqual(chess.played, False)
        player.click((1, 2))
        self.assertEqual(chess.played, True)

    def test_input_player_confirm_draw(self):
        timer = MockTimer()
        chess = MockChess()
        player = InputPlayer(WHITE, timer, chess)
        player.confirm_draw()
        self.assertEqual(chess.confirm_draw, player)

class TestAIPlayer(unittest.TestCase):

    def test_new_ai_player(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, RANDOM)
        self.assertEqual(player.level, RANDOM)
        self.assertNotEqual(player.openings, {})

    def test_ai_player_start_turn(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, RANDOM)
        openings = player.openings
        player.start_turn()
        self.assertEqual(timer.turn_started, True)
        sleep(0.12)
        self.assertEqual(player.openings, openings)
        self.assertNotEqual(chess.selected, None)
        self.assertEqual(chess.played, True)

    def test_ai_player_semi_random_move(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, SEMI_RANDOM)
        openings = player.openings
        player.ai_move()
        self.assertEqual(player.openings, openings)
        self.assertNotEqual(chess.selected, None)
        self.assertEqual(chess.played, True)


    def test_ai_player_opening_move(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, EASY)
        openings = player.openings
        player.ai_move()
        self.assertNotEqual(player.openings, openings)
        self.assertNotEqual(chess.selected, None)
        self.assertEqual(chess.played, True)

    def test_ai_player_negamax(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, EASY)
        player.openings = {}
        player.ai_move()
        self.assertNotEqual(chess.selected, None)
        self.assertEqual(chess.played, True)

    def test_ai_player_deny_draw(self):
        timer = MockTimer()
        chess = MockChess()
        player = AIPlayer(WHITE, timer, chess, RANDOM)
        player.confirm_draw()
        self.assertEqual(chess.draw_denied, player)


class TestPlayer(TestBasePlayer,
                 TestInputPlayer,
                 TestAIPlayer):
    pass