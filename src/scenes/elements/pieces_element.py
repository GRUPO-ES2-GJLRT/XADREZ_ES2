# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .chess_element import ChessElement
from .others import LazyAttribute


class PiecesElement(ChessElement):

    square_size = LazyAttribute("_square_size")
    piece_images = LazyAttribute("_piece_images")
    board = LazyAttribute("_board")

    def __init__(self, board, square_size, piece_images,
                 x=0, y=0, children=None, condition=None, name=""):
        super(PiecesElement, self).__init__(x, y, children, condition, name)

        self.board = board
        self.square_size = square_size
        self.piece_images = piece_images

    def draw_element(self, screen, x=0, y=0):
        for piece in self.board.get_pieces():
            screen.blit(
                self.piece_images['%s_%s' %
                                  (piece.color, piece.name)].get(),
                self.position_rect(piece.position, x=x, y=y)
            )

    def start_x(self):
        return min(0, super(PiecesElement, self).start_x())

    def start_y(self):
        return min(0, super(PiecesElement, self).start_y())

    def width(self):
        return max(self.square_size * 8, super(PiecesElement, self).width())

    def height(self):
        return max(self.square_size * 8, super(PiecesElement, self).height())
