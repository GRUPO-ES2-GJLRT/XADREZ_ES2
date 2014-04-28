# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .piece import Piece
from consts.moves import NORMAL, NO_ATTACK, ATTACK, ALL


class Knight(Piece):

    def name(self):
        return 'knight'

    def get_positions(self):
        return [
            (self.x - 2, self.y - 1), (self.x - 2, self.y + 1),
            (self.x - 1, self.y - 2), (self.x - 1, self.y + 2),
            (self.x + 2, self.y - 1), (self.x + 2, self.y + 1),
            (self.x + 1, self.y - 2), (self.x + 1, self.y + 2),
        ]

    def get_valid_no_attack_moves(self):
        return [
            (self.position, position)
            for position in self.get_valid_positions()
            if self.board.is_valid_position(position) and self.board.is_empty_position(position)
        ]

    def get_valid_attack_moves(self):
        return [
            (self.position, position)
            for position in self.get_valid_positions()
            if self.board.is_valid_position(position) and self.board.is_enemy_position(position, self.color)
        ]

    def get_valid_moves(self):
        return [
            (self.position, position)
            for position in self.get_valid_positions()
            if self.board.is_valid_position(position) and not self.board.is_friendly_position(position, self.color)
        ]

    def possible_moves(self, hindered=True, hindered_positions=None):
        move = {}
        enemy = {}
        _, allowed = self.get_allowed()
        for position in self.get_positions():
            if not self.board.is_valid_position(position):
                continue
            if not position in allowed:
                continue
            temp = move
            piece = self.board[position]
            if piece and not piece.ignored:
                if piece.color == self.color:
                    continue
                else:
                    temp = enemy
            temp[position] = NORMAL
        return move, enemy

    def optimized_possible_moves(self, move_type, queue):
        if move_type == ALL:
            queue.put(self.get_valid_moves())
        elif move_type == NO_ATTACK:
            queue.put(self.get_valid_no_attack_moves())
        elif move_type == ATTACK:
            queue.put(self.get_valid_attack_moves())
        else:
            queue.put([])
