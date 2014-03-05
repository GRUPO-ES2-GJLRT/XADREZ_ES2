# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import sys, os

class Scene(object):

    def __init__(self, game):
        """ Scene constructor 

        Arguments:
        game is a Game instance
        """
        self.assets_dir = os.path.join(sys.argv[0], '..', '..', 'assets')
        self.game = game

    def loop(self, delta_time):
        """This function is called in the game loop.

        Arguments:
        delta_time is the time in seconds (float) passed since 
            the last execution

        It calls the method self.event for each event and calls the method
            self.draw once to draw the screen
        """
        self.game.screen.fill((0, 0, 0))

        self.draw(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            else:
                self.event(delta_time, event)

        pygame.display.flip()

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


class GameText(object):

    def __init__(self, font, text, antialias, color, rect=None):
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = None
        self.redraw()
        self.rect = self.surface.get_rect()
        if rect:
            self.rect = rect
        
    def redraw(self):
        self.surface = self.font.render(self.text, self.antialias, self.color)

    def blit(self, screen):
        screen.blit(self.surface, self.rect.topleft)

