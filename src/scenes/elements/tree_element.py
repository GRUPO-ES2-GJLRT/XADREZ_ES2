# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .game_div import GameDiv
from .game_text_element import GameTextElement
from .others import Font
from consts.colors import WHITE
from pygame import draw


class TreeElement(GameDiv):

    def __init__(self, node=None, size=25, space=30, counter=1,
                 x=0, y=0, children=None, condition=None, name=''):
        super(TreeElement, self).__init__(x, y, children, condition, name)
        self.node = node
        self.size = size
        self.space = space
        self.counter = counter
        self.populate_children(self.x, self.y)

    def populate_children(self, x, y):
        if not self.node:
            return
        text_color = (255, 255, 255) if self.color == (0, 0, 0) else (0, 0, 0)
        self.children = [
            GameTextElement(
                x=self.size // 2, y=self.size // 2, text=str(self.node.value),
                font=Font(size=13), color=text_color
            ),
        ]
        y = self.space
        for child in self.node.childs:
            sub_tree = TreeElement(
                node=child, x=self.space, y=y, size=self.size,
                space=self.space
            )
            self.children.append(sub_tree)
            y += sub_tree.height()

    @property
    def color(self):
        if self.node and self.node.color == WHITE:
            return (255, 255, 255)
        else:
            return (0, 0, 0)

    def draw_element(self, screen, x=0, y=0):
        self.populate_children(x, y)
        draw.rect(screen, self.color, (x, y, self.size, self.size))

    def start_x(self):
        return min(0, super(TreeElement, self).start_x())

    def start_y(self):
        return min(0, super(TreeElement, self).start_y())

    def width(self):
        return max(self.space, super(TreeElement, self).width())

    def height(self):
        return max(self.space, super(TreeElement, self).height())
