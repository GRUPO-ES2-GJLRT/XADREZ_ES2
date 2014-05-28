# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import time
import pygame
from optparse import OptionParser
from pygame.locals import (
    HWSURFACE, DOUBLEBUF, RESIZABLE
)

from consts.i18n import (
    TITLE, CREATE_ARG, CREATE_HELP, JOIN_ARG, JOIN_HELP,
    CREATE_JOIN_ERROR
)
from game_elements.ai_player import LEVEL_MAP

from scenes.online_chess import OnlineChess

WIDTH, HEIGHT = 512, 384


class Game(object):

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.resize((width, height))
        self.running = True
        self.scene = None
        from scenes.main_menu import MainMenu
        self.scene = MainMenu(self)


    def loop(self):
        last_frame_time = 0
        #import yappi
    
        #yappi.start()
        while self.running:
    
            current_time = time.time()
            delta_time = current_time - last_frame_time
            last_frame_time = current_time

            self.scene.loop(delta_time)
        
        self.scene.close()

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
    parser = OptionParser()
    parser.add_option('-c', '--create', dest="create", metavar=CREATE_ARG,
                      help=CREATE_HELP)
    parser.add_option('-j', '--join', dest="join",
                      help=JOIN_HELP, nargs=2, metavar=JOIN_ARG) 
    (opts, args) = parser.parse_args()
    game = Game(WIDTH, HEIGHT)
    if opts.create and opts.join:
        print(CREATE_JOIN_ERROR)
        parser.print_help()
        exit(-1)
    elif opts.create:
        black = -1
        white = LEVEL_MAP[opts.create]
        chess = OnlineChess(game, white, black)
        print(chess.game_id)
        game.scene = chess
    elif opts.join:
        white = -1
        black = LEVEL_MAP[opts.join[1]]
        chess = OnlineChess(game, white, black, int(opts.join[0]))
        print(chess.game_id)
        game.scene = chess
    game.loop()
