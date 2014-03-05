# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King


class Board(object):
    def __init__(self, new_game=True):
        self.board_data = [
            [None for x in xrange(8)] for y in xrange(8)
        ]
        self.pieces = {
            'white': [],
            'black': [],
        }
        if new_game:
            # Pawn
            for x in xrange(8):
                Pawn(self, 'white', x, 1)
                Pawn(self, 'black', x, 6)
            # Rook
            Rook(self, 'white', 0, 0)
            Rook(self, 'white', 7, 0)
            Rook(self, 'black', 0, 7)
            Rook(self, 'black', 7, 7)
            # Knight
            Knight(self, 'white', 1, 0)
            Knight(self, 'white', 6, 0)
            Knight(self, 'black', 1, 7)
            Knight(self, 'black', 6, 7)
            # Bishop
            Bishop(self, 'white', 2, 0)
            Bishop(self, 'white', 5, 0)
            Bishop(self, 'black', 2, 7)
            Bishop(self, 'black', 5, 7)
            # Queen
            Queen(self, 'white', 3, 0)
            Queen(self, 'black', 3, 7)
            # King
            King(self, 'white', 4, 0)
            King(self, 'black', 4, 7)

    def __getitem__(self, position):
        """ Access the board position 
        Usage: board[(x, y)]
        """
        if not self.valid(position):
            return None
        return self.board_data[position[0]][position[1]] 

    def add(self, piece):
    	""" Add piece to the board.
        This is called in the creation of Piece.
        """
        self.board_data[piece.x][piece.y] = piece
        self.pieces[piece.color].append(piece)

    def remove(self, position):
        """ Remove piece from board. """
        piece = self[position[0]][position[1]]
        if piece:
            self.board_data[piece.x][piece.y] = None    
            self.pieces[piece.color].remove(piece)


    def valid(self, position):
    	""" Checks if position tuple is inside the board """
    	return 0 <= position[0] < 8 and 0 <= position[1] < 8 
