# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame
import sys
import os
import json


from consts.default import (
    TIMER, MINUTES, MOVES, BONUS, FIFTY_MOVE, JIT_DRAW, TIMEOUT
)


class Scene(object):

    def __init__(self, game):
        """ Scene constructor

        Arguments:
        game is a Game instance
        """
        self.data_dir = os.path.abspath(
            os.path.join(sys.argv[0], '..', '..', 'data'))
        self.game = game
        self.jit_draw = False
        self.should_draw = True
        self.thread_events = []

    def loop(self, delta_time):
        """This function is called in the game loop.

        Arguments:
        delta_time is the time in seconds (float) passed since
            the last execution

        It calls the method self.event for each event and calls the method
            self.draw once to draw the screen
        """

        self.draw(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                self.close()
            elif event.type == pygame.VIDEORESIZE:
                self.game.resize(event.dict['size'])
                self.resize()
                self.game.screen.fill((0, 0, 0))
                self.draw(0)
                pygame.display.flip()
            else:
                self.event(delta_time, event)

        pygame.display.flip()

    def do_jit_draw(self):
        self.should_draw = True

    def load_stored_config(self):
        data = {
            'timer': TIMER,
            'minutes': MINUTES,
            'moves': MOVES,
            'bonus': BONUS,
            'fifty_move': FIFTY_MOVE,
            'jit_draw': JIT_DRAW,
            'timeout': TIMEOUT
        }

        file_path = os.path.abspath(os.path.join(self.data_dir, 'config.json'))
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data.update(json.load(f))
        return data

    def set_text_position(self, text, x, y):
        text.rect = self.place_rect(
            text.surface,
            self.game.relative_x(x),
            self.game.relative_y(y),
        )

    def place_rect(self, text, x, y):
        rect = text.get_rect()
        rect.center = (x, y)
        return rect

    def center_rect(self, text, y):
        """Returns the text rect in position (center, y) """
        rect = text.get_rect()
        rect.center = (
            self.game.screen.get_rect().center[0],
            y
        )
        return rect

    def draw(self, delta_time):
        """This function should draw the scene.
        Override it in a subclass!

        Arguments:
        delta_time is the time in seconds (float) passed since
            the last game loop execution
        """
        pass

    def event(self, delta_time, event):
        """This function should process the events.
        Override it in a subclass!

        Arguments:
        game is a Game instance
        delta_time is the time in seconds (float) passed since
            the last game loop execution
        event is the received event
        """
        pass

    def resize(self):
        """This function should resize the elements.
        Override it in a subclass!
        """
        pass

    def free_events(self):
        for threaded_event in self.thread_events:
            threaded_event.set()

    def close(self):
        self.game.running = False
        #import yappi
        #yappi.get_func_stats().print_all()
        #yappi.get_thread_stats().print_all()

        self.free_events()
        sys.exit()
