# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

class Board(object):
    def __init__(self, new_game=True):
        self.board_data = [
            [None for x in xrange(8)] for y in xrange(8)
        ]

    def __getitem__(self, position):
        """ Access the board position 
        Usage: board[(x, y)]
        """
        return self.board_data[position[0]][position[1]] 

    def add(self, piece):
    	""" Add piece to the board.
        This is called in the creation of Piece.
        """
        self.board_data[piece.x][piece.y] = piece

    def valid(self, position):
    	""" Checks if position tuple is inside the board """
    	return 0 <= position[0] < 8 and 0 <= position[1] < 8 