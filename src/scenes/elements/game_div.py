# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals


class GameDiv(object):

    def __init__(self, x=0, y=0, children=None, condition=None, name=""):
        if not children:
            children = []
        if not condition:
            condition = lambda: True
        self.condition = condition
        self.x = x
        self.y = y
        self.children = children
        self.name = name

    def draw(self, screen, x=0, y=0):
        if not self.condition():
            return
        self.draw_element(screen, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.draw(screen, x=self.x + x, y=self.y + y)

    def click(self, pos, x=0, y=0):
        if not self.condition():
            return
        self.click_element(pos, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.click(pos, x=self.x + x, y=self.y + y)

    def motion(self, pos, x=0, y=0):
        if not self.condition():
            return
        self.motion_element(pos, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.motion(pos, x=self.x + x, y=self.y + y)

    def draw_element(self, screen, x=0, y=0):
        pass

    def click_element(self, pos, x=0, y=0):
        pass

    def motion_element(self, pos, x=0, y=0):
        pass