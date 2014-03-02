# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

class Board(object):
    def __init__(self, new_game=True):
        self.board_data = [
            [None for x in xrange(8)] for y in xrange(8)
        ]

    def add(self, piece):
        self.board_data[piece.x][piece.y] = piece

    def __getitem__(self, position):
        return self.board_data[position[0]][position[1]] 
