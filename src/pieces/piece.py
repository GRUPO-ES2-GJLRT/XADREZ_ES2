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

    def possible_moves(self, hindered=True, hindered_positions=None):
        """ Return the possible moves for the piece
        hindered: It may check for hindered positions on board
        """
        pass

    def valid_move(self, position):
        """ Checks if a position is not occupied by an ally
        and is inside the board
        """
        if not self.board.valid(position):
            return False
        piece = self.board[position]
        if piece and not piece.ignored and piece.color == self.color:
            return False
        return True

    def is_hindered(self, position=None, hindered=None):
        """ Checks if a position is hindered by an enemy
        If not provided, position is the piece position
        """
        if position is None:
            position = self.position
        position = (position[0], position[1])
        if hindered is None:
            hindered = self.board.hindered(next(self.color))
        return position in hindered
