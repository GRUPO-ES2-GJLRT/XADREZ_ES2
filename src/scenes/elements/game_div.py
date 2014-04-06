# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .others import LazyAttribute


class GameDiv(object):

    x = LazyAttribute('_x')
    y = LazyAttribute('_y')

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

    def call(self, name):
        method = getattr(self, name, None)
        if callable(method):
            method()
        for child in self.children:
            child.call(name)

    def draw(self, screen, x=0, y=0):
        if not self.condition():
            return
        self.draw_element(screen, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.draw(screen, x=self.x + x, y=self.y + y)

    def click(self, pos, x=0, y=0):
        if not self.condition():
            return
        clicked = self.click_element(pos, x=self.x + x, y=self.y + y)
        if clicked:
            return clicked
        for child in self.children:
            clicked = child.click(pos, x=self.x + x, y=self.y + y)
            if clicked:
                return clicked

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

    def start_x(self):
        return (min(child.x + child.start_x() for child in self.children)
                if self.children else 0)

    def start_y(self):
        return (min(child.y + child.start_y() for child in self.children)
                if self.children else 0)

    def width(self):
        return (max(c.x + c.width() + c.start_x()
                    for c in self.children) - self.start_x()
                if self.children else 0)

    def height(self):
        return (max(c.y + c.height() + c.start_y()
                    for c in self.children) - self.start_y()
                if self.children else 0)
