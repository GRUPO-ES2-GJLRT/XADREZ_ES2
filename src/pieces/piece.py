# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

class Piece(object):

    def __init__(self, board, color, x, y):
        self.board = board
        self.color = color
        self.x = x
        self.y = y
        board.add(self)

    def possible_moves(self):
        """ Return the possible moves for the piece """
        pass