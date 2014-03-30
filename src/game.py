# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import time
import pygame
from pygame.locals import (
    HWSURFACE, DOUBLEBUF, RESIZABLE
)

from consts.i18n import TITLE

WIDTH, HEIGHT = 1024, 768


class Game(object):

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.resize((width, height))
        self.running = True
        self.scene = None

    def loop(self):
        from scenes.main_menu import MainMenu
        self.scene = MainMenu(self)
        last_frame_time = 0

        while self.running:
            current_time = time.time()
            delta_time = current_time - last_frame_time
            last_frame_time = current_time

            self.scene.loop(delta_time)

    def resize(self, size):
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              HWSURFACE | DOUBLEBUF |
                                              RESIZABLE)

    def __relative(self, value, size):
        result = value * size
        return int(max(0, min(size - 1, result)))

    def center_x(self):
        return self.screen.get_rect().center[0]

    def center_y(self):
        return self.screen.get_rect().center[1]

    def relative_x(self, x):
        """Returns the coordinate X relative to the screen width
        Arguments:
        x: float [0..1]
        """
        return self.__relative(x, self.width)

    def relative_y(self, y):
        """Returns the coordinate Y relative to the screen height
        Arguments:
        y: float [0..1]
        """
        return self.__relative(y, self.height)

if __name__ == '__main__':
    game = Game(WIDTH, HEIGHT)
    game.loop()
