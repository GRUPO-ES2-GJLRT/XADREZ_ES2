# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pygame import draw
from.game_div import GameDiv, LazyAttribute


class RectElement(GameDiv):

    size_x = LazyAttribute("_size_x")
    size_y = LazyAttribute("_size_y")

    def __init__(self, color, size_x, size_y,
                 x=0, y=0, children=None, condition=None, name=""):
        super(RectElement, self).__init__(x, y, children, condition, name)

        self.color = color
        self.size_x = size_x
        self.size_y = size_y

    def draw_element(self, screen, x=0, y=0):
        draw.rect(screen, self.color, (x, y, self.size_x, self.size_y))