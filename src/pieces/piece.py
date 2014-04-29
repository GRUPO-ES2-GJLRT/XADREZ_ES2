# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from consts.colors import next


class Piece(object):

    def __init__(self, board, color, x, y):
        self.board = board
        self.color = color
        self.x = x
        self.y = y
        self.has_moved = False
        self.ignored = False
        board.add(self)

    @property
    def name(self):
        """ Return the piece name used by the image """
        pass

    @property
    def position(self):
        """ Return the piece position x, y """
        return (self.x, self.y)

    @position.setter
    def position(self, value):
        """ sets x, y """
        self.x = value[0]
        self.y = value[1]

    def possible_moves(self):
        """ Return the possible moves for the piece """
        pass

    def attack_moves(self):
        """ Return the attack moves for the piece """
        moves, attack = self.possible_moves()
        moves.update(attack)
        return moves

    def optimized_possible_moves(self, move_type, queue):
        """ Return the possible moves for the piece
        type: 0 = Non-Attacking moves | 1 = Attacking Moves | 2 = All moves
        queue: None = function will just normally return |
            Queue() = function will store the return value queue, then return
        """
        pass

    def valid_move(self, position):
        """ Checks if a position is not occupied by an ally
        and is inside the board
        """
        if not self.board.is_valid_position(position):
            return False
        piece = self.board[position]
        if piece and not piece.ignored and piece.color == self.color:
            return False
        return True

    def get_allowed(self):
        self.ignored = True
        if self.board.kings[self.color]:
            position = self.board.kings[self.color].position
        else:
            position = (-1, -1)
        _, allowed = self.board.hindered_position(position, next(self.color))
        self.ignored = False
        return _, allowed
