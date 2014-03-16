# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import sys, os, json

from consts.default import TIMER, MINUTES, MOVES, BONUS

class Scene(object):

    def __init__(self, game):
        """ Scene constructor 

        Arguments:
        game is a Game instance
        """
        self.assets_dir = os.path.join(sys.argv[0], '..', '..', 'assets')
        self.data_dir = os.path.join(sys.argv[0], '..', '..', 'data')
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

    def load_stored_config(self):
        data = {
            'option': TIMER,
            'minutes': MINUTES,
            'moves': MOVES,
            'bonus': BONUS,
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



class GameText(object):

    def __init__(self, font, text, antialias, color, rect=None, style="normal", other_color=None):
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = None
        self.style = style
        self.other_color = other_color if other_color else self.color
        self.redraw()
        self.rect = self.surface.get_rect()
        if rect:
            self.rect = rect
        
    def hollow(self):
        notcolor = [c^0xFF for c in self.other_color]
        base = self.font.render(self.text, 0, self.other_color, notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = pygame.Surface(size, 16)
        img.fill(notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)
        return img

    def redraw(self):
        if self.style == "hollow":
            self.surface = self.hollow()
        elif self.style == "outline":
            base = self.font.render(self.text, 0, self.color)
            outline = self.hollow()
            img = pygame.Surface(outline.get_size(), 16)
            img.blit(base, (1, 1))
            img.blit(outline, (0, 0))
            img.set_colorkey(0)
            self.surface = img
        else:
            self.surface = self.font.render(self.text, self.antialias, self.color)

    def blit(self, screen):
        screen.blit(self.surface, self.rect.topleft)

