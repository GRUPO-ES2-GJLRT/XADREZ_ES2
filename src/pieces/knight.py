# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .piece import Piece
from consts.moves import NORMAL, NO_ATTACK, ATTACK


class Knight(Piece):

    def name(self):
        return "knight"

    def get_valid_move_positions(self):
        positions = [
            (self.x - 2, self.y - 1), (self.x - 2, self.y + 1),
            (self.x - 1, self.y - 2), (self.x - 1, self.y + 2),
            (self.x + 2, self.y - 1), (self.x + 2, self.y + 1),
            (self.x + 1, self.y - 2), (self.x + 1, self.y + 2),
        ]

        return [
            position for position in positions
            if not self.board.is_friendly_position(position, self.color)
        ]

    def possible_moves(self, hindered=True, hindered_positions=None):
        moves = self.get_valid_move_positions()

        return {position: NORMAL for position in moves
                if self.valid_move(position)}

    def optimized_possible_moves(self, move_type, queue=None):
        moves = []
        valid_positions = self.get_valid_move_positions()

        if move_type == NO_ATTACK:
            for position in valid_positions:
                if self.board.is_empty_position(position):
                    moves.append((self.position, position))

        elif move_type == ATTACK:
            for position in valid_positions:
                if self.board.is_enemy_position(position, self.color):
                    moves.append((self.position, position))

        else:
            moves = [(self.position, position) for position in valid_positions]

        if queue:
            queue.put(moves)

        return moves

