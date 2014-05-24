# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .game_div import GameDiv
import pygame


class SnapElement(GameDiv):

    def __init__(self,
                 x=0, y=0, children=None, condition=None, name=''):
        super(SnapElement, self).__init__(x, y, children, condition, name)
        self.show_snap = False
        self.change_snap = 0
        self.image = None

    def draw(self, screen, x=0, y=0):
        if self.change_snap == 1:
            super(SnapElement, self).draw(screen, x, y)
            w, h = int(self.width()), int(self.height())
            rect = pygame.Rect(x, y, w, h)
            self.image = pygame.Surface((w, h))
            self.image.blit(screen, area=rect, dest=(0, 0))
            self.show_snap = True
            self.change_snap = 0
        if self.change_snap > 0:
            self.change_snap -= 1
        if not self.show_snap:
            super(SnapElement, self).draw(screen, x, y)
        else:
            if not self.condition():
                return
            screen.blit(self.image, (x, y))

    def snap(self):
        self.change_snap = 10

    def dynamic(self):
        self.show_snap = False

    def start_x(self):
        return min(0, super(SnapElement, self).start_x())

    def start_y(self):
        return min(0, super(SnapElement, self).start_y())
