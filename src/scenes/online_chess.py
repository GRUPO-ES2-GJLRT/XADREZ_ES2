# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import urllib
import urllib2
import sys
import logging
import threading
from time import sleep, time
from scenes.chess import Chess
from cython.functions import tuple_to_chess_notation, chess_notation_to_tuple
from consts.colors import BLACK, WHITE, next
from consts.urls import (
	URL_BASE,
	NEW_GAME,
	JOIN_GAME,
	NEW_MOVE,
	WAITING_MOVE_VALIDATION,
	VALIDATE_MOVE,
	SHOW_MOVE,
	NEW_GAME_OVER_REQUEST,
	WAITING_GAME_OVER_VALIDATION,
	SHOW_GAME_OVER,
	SUCCESS,
	SUCCESS_CODES
)
from consts.pieces import (
	PAWN,
	KNIGHT,
	BISHOP,
	ROOK,
	QUEEN,
	KING,
)



INVALID_REQUEST = "INVALID REQUEST"
INVALID_TURN = "INVALID TURN"

PROMOTION_MAP = {
	0: ROOK,
	1: KNIGHT,
	2: BISHOP,
	3: QUEEN,
	4: KING,
	5: PAWN
}


def html_request(url, method, values={}):
	try:
		data = urllib.urlencode(values)
		request = urllib2.Request(url, data)
		request.get_method = lambda: method
		result = json.load(urllib2.urlopen(request))
		if not result['code'] in SUCCESS_CODES:
			raise Exception(INVALID_REQUEST, result['code'], result['message'])
		if not result['code'] == 19:
			if 'board' in result:
				del result['board']
			print(time(), result)
		return result
	except Exception as e:
		logging.exception('URL {0} {1}\n{3}\n{2}'.format(
			method, url, str(e), values
		))
		raise e

def post(url, values={}):
	return html_request(url, 'POST', values)

def get(url, values={}):
	return html_request(url, 'GET', values)

class OnlineChess(Chess):

	def __init__(self, game, level_white, level_black, id=None, *args, **kwargs):
		if level_white != -1:
			data = post(URL_BASE + NEW_GAME, {'player_name': 'wgrupo1'})
			self.online = BLACK
			self.player_key = data['player_key']
			self.game_id = data['game_id']
			self.player_name = 'wgrupo1'

		if level_black != -1:
			self.game_id = id
			data = post(URL_BASE + JOIN_GAME, {
				'player_name': 'bgrupo1',
				'game_id': self.game_id,
			})
			self.online = WHITE
			self.player_key = data['player_key']
			self.player_name = 'bgrupo1'
		self.sent_end_game = False
		super(OnlineChess, self).__init__(game, level_white, level_black, *args, **kwargs)
		threading.Thread(target=self.wait_end_game_validation).start()

	def do_move(self, selected, square, promotion=5):
		color = self.board.color()
		move = self.board.move(selected, square, promotion)
		if self.online == color:
			data = post(URL_BASE + VALIDATE_MOVE, {
				'move_id': self.move_id,
				'player_key': self.player_key,
				'valid': 'true' if move else 'false'
			})
			return move
		elif move:
			move_type = move.type()
			param = {
				'game_id': self.game_id,
				'player_key': self.player_key,
				'type': move_type
			}
			if move_type in [0, 2, 3]:
				param['move_from'] = tuple_to_chess_notation(selected)
				param['move_to'] = tuple_to_chess_notation(square)
			if move_type == 1: #castling
				param['rook_from'] = tuple_to_chess_notation(move.rook_from())
				param['rook_to'] = tuple_to_chess_notation(move.rook_to())
				param['king_from'] = tuple_to_chess_notation(selected)
				param['king_to'] = tuple_to_chess_notation(square)

			if move_type == 2: #en passant
				param['eliminated_pawn'] = tuple_to_chess_notation(
					move.get_eliminated_pawn())
			if move_type == 3: #promotion
				param['promotion_type'] = 3 #queen


			data = post(URL_BASE + NEW_MOVE, param)
			self.move_id = data['move']['id']
			while self.running:
				self.do_jit_draw()
				data = get(URL_BASE + SHOW_MOVE.format(self.move_id))
				if data['move']['validation_time']:
					if not data['move']['legal']:
						move.undo_update(self.board)
						return False
					else:
						return move
				sleep(3)
		return False


	def wait_move_validation(self):
		while self.running:
			data = get(URL_BASE + WAITING_MOVE_VALIDATION, {
				'game_id': self.game_id
			})
			if 'move' in data:
				self.move_id = data['move']['id']
				move_type = data['move']['move_type']
				move = data['move']['movimentations'][0]
				if move_type == 1: #castling
					for move in data['move']['movimentations']:
						if move['from'] in ['e1', 'e8']:
							return (
								chess_notation_to_tuple(move['from']),
								chess_notation_to_tuple(move['to']),
								5
							)
				elif move_type == 3: #promotion
					return (
						chess_notation_to_tuple(move['from']),
						chess_notation_to_tuple(move['to']),
						PROMOTION_MAP[data['move']['promotion_type']]
					)
				return (
					chess_notation_to_tuple(move['from']),
					chess_notation_to_tuple(move['to']),
					5
				)
			sleep(3)

	def wait_end_game_validation(self):
		while self.running:
			if self.sent_end_game:
				continue
			data = get(URL_BASE + WAITING_GAME_OVER_VALIDATION, {
				'game_id': self.game_id
			})
			if 'game_over_request' in data:
				request = data['game_over_request']
				if request['winner'] == self.player_name:
					self.end_game(1 if self.online == BLACK else -1)
				else:
					end = self.verify_status(self.board.status(None))
					if not end:
						if not request['winner']:
							self.sent_end_game = True
							self.other_player.confirm_draw()
						else:
							self.send_illigal_endgame()
							

	def request_draw(self):
		self.end_game(0)

	def send_illigal_endgame(self):
		post(URL_BASE + NEW_GAME_OVER_REQUEST, {
			'game_id': self.game_id,
			'player_key': self.player_key,
			'result': 1
		})

	def deny_draw(self, player, send=True):
		if send:
			self.send_illigal_endgame()
		Chess.deny_draw(self, player)
		self.sent_end_game = False

	def end_game(self, state):
		self.sent_end_game = True
		data = post(URL_BASE + NEW_GAME_OVER_REQUEST, {
			'game_id': self.game_id,
			'player_key': self.player_key,
			'result': state * (1 if self.online == BLACK else -1)
		})
		self.game_over_request_id = data['game_over_request_id']
		if data['code'] == 14:
			Chess.end_game(self, state)
		while self.running:
			data = get(URL_BASE + SHOW_GAME_OVER.format(
				self.game_over_request_id
			))
			if data['game_over_request']['validation_time']:
				if data['game_over_request']['legal']:
					Chess.end_game(self, state)
					#self.sent_end_game = False
				else:
					self.deny_draw(self.current_player, send=False)
				return None
			sleep(3)
	
