# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .chess_element import ChessElement


class PiecesElement(ChessElement):
    def __init__(self, board, square_size, piece_images,
                 x=0, y=0, children=None, condition=None, name=""):
        super(PiecesElement, self).__init__(x, y, children, condition, name)

        self.board = board
        self.square_size = square_size
        self.piece_images = piece_images

    def draw_element(self, screen, x=0, y=0):
        for color, pieces in self.board.pieces.items():
            for piece in pieces:
                screen.blit(
                    self.piece_images['%s_%s' % (piece.color, piece.name())],
                    self.position_rect(piece.position, x=x, y=y)
                )
