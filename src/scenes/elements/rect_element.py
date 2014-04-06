# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pygame import draw
from.game_div import GameDiv
from .others import LazyAttribute


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

    def start_x(self):
        return min(0, super(RectElement, self).start_x())

    def start_y(self):
        return min(0, super(RectElement, self).start_y())

    def width(self):
        return max(self.size_x, super(RectElement, self).width())

    def height(self):
        return max(self.size_y, super(RectElement, self).height())
