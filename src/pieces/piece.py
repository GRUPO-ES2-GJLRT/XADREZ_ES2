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

    def valid_move(self, position):
    	""" Checks if a position is not occupied by an ally 
    	and is inside the board 
    	"""
        if not self.board.valid(position):
            return False
        piece = self.board[position]
        if piece and piece.color == self.color:
            return False
        return True