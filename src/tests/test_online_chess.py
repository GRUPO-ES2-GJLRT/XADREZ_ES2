# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

import scenes.online_chess
from consts.colors import WHITE, BLACK
from consts.pieces import PAWN, KING
from consts.urls import (
    URL_BASE,
    NEW_GAME,
    JOIN_GAME,
    SHOW_MOVE,
    NEW_MOVE,
    WAITING_MOVE_VALIDATION,
    VALIDATE_MOVE,
    NEW_GAME_OVER_REQUEST,
    WAITING_GAME_OVER_VALIDATION,
    SHOW_GAME_OVER,
    SUCCESS,
    SUCCESS_CODES,

)


valid_html_request = lambda url, m, v={}: {
    (URL_BASE + NEW_GAME): {'player_key': 'a', 'game_id': 2, 'code': 0},
    (URL_BASE + JOIN_GAME): {'player_key': 'b', 'code': 0},
    (URL_BASE + SHOW_MOVE.format(1)): {'move': {'validation_time': '2014', 
                                                'legal': 1,}, 
                                       'code': 0},
    (URL_BASE + NEW_MOVE): {'code': 0, 'move': {"id": 1}},
    (URL_BASE + WAITING_MOVE_VALIDATION): {'code': 0, 'move': {
        "id": 1, "move_type": 0,
        "movimentations": [{'from': 'c1', 'to': 'c3'}]}},
    (URL_BASE + VALIDATE_MOVE): {'code': 0},
    (URL_BASE + NEW_GAME_OVER_REQUEST): {'code': 0, 'game_over_request_id': 1},
    (URL_BASE + WAITING_GAME_OVER_VALIDATION): {'code': 0},
    (URL_BASE + SHOW_GAME_OVER): {'code': 0, 'game_over_request': {
        'validation_time': '2014', 'legal': 0
    }},
    
}[url]

invalid_sent_move = lambda url, m, v={}: {
    (URL_BASE + NEW_GAME): {'player_key': 'a', 'game_id': 2, 'code': 0},
    (URL_BASE + JOIN_GAME): {'player_key': 'b', 'code': 0},
    (URL_BASE + SHOW_MOVE.format(1)): {'move': {'validation_time': '2014', 
                                                'legal': 0,}, 
                                       'code': 0},
    (URL_BASE + NEW_MOVE): {'code': 0, 'move': {"id": 1}},
    (URL_BASE + WAITING_MOVE_VALIDATION): {'code': 0, 'move': {
        "id": 1, "move_type": 0,
        "movimentations": [{'from': 'c1', 'to': 'c3'}]}},
    (URL_BASE + VALIDATE_MOVE): {'code': 0},
    (URL_BASE + NEW_GAME_OVER_REQUEST): {'code': 0, 'game_over_request_id': 1},
    (URL_BASE + WAITING_GAME_OVER_VALIDATION): {'code': 0},
    (URL_BASE + SHOW_GAME_OVER): {'code': 0, 'game_over_request': {
        'validation_time': '2014', 'legal': 0
    }},
}[url]

class GameStub(object):

    def __init__(self):
        self.running = True
        self.width = 1024
        self.height = 768




OnlineChess = scenes.online_chess.OnlineChess

class TestOnlineChessCreate(unittest.TestCase):


    def test_create_new_game(self):
        game = GameStub()
        scenes.online_chess.html_request = valid_html_request
        oc = OnlineChess(game, 0, -1)
        self.assertNotEqual(oc.player_key, None)
        self.assertNotEqual(oc.game_id, None)
        self.assertEqual(oc.online, BLACK)
        oc.free_events()
        game.running = False

    def test_join_game(self):
        game = GameStub()
        scenes.online_chess.html_request = valid_html_request
        oc = OnlineChess(game, -1, 0, 1)
        self.assertNotEqual(oc.player_key, None)
        self.assertNotEqual(oc.game_id, None)
        self.assertEqual(oc.online, WHITE)
        oc.free_events()
        game.running = False

    def test_do_move_send_move_and_wait_for_legal_validation(self):
        game = GameStub()
        scenes.online_chess.html_request = valid_html_request
        oc = OnlineChess(game, 0, -1)
        self.assertTrue(oc.do_move((0, 1), (0, 3)))
        self.assertEqual(oc.move_id, 1)
        oc.free_events()
        game.running = False

    def test_do_move_send_move_and_wait_for_illegal_validation(self):
        game = GameStub()
        scenes.online_chess.html_request = invalid_sent_move
        oc = OnlineChess(game, 0, -1)
        self.assertFalse(oc.do_move((0, 1), (0, 3)))
        self.assertEqual(oc.move_id, 1)
        oc.free_events()
        game.running = False

   
class TestOnlineChess(TestOnlineChessCreate):
    pass