# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from pygame import draw
from .chess_element import ChessElement


class SquareElement(ChessElement):
    def __init__(self, color, square_size, square,
                 x=0, y=0, children=None, condition=None, name=""):
        super(SquareElement, self).__init__(x, y, children, condition, name)

        self.color = color
        self.square = square
        self.square_size = square_size

    def draw_element(self, screen, x=0, y=0):
        square = self.square()
        if square:
            draw.rect(screen, self.color,
                self.position_rect(square, x=x, y=y))