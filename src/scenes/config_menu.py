# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

from .base import Scene, GameText
from locales.i18n import *


class ConfigMenu(Scene):

    def __init__(self, *args, **kwargs):
        """ConfigMenu constructor. Creates texts and buttons"""
        super(ConfigMenu, self).__init__(*args, **kwargs)

        # Title
        title_font = pygame.font.SysFont("", self.game.relative_x(0.1))
        title = GameText(title_font, CONFIG, True, (192, 192, 192))
        title.rect = self.center_rect(
            title.surface, 
            self.game.relative_y(0.1)
        )
        
        menu_font = pygame.font.SysFont("", self.game.relative_x(0.05))

        # Back Button
        back = GameText(menu_font, BACK, True, (128, 128, 128))
        back.rect = self.place_rect(
            back.surface,
            self.game.relative_x(0.10),
            self.game.relative_y(0.92),
        )

        def back_click(game):
            from .main_menu import MainMenu
            game.scene = MainMenu(game)

        back.click = back_click

        # Quit Button
        quit = GameText(menu_font, QUIT, True, (128, 128, 128))
        quit.rect = self.place_rect(
            quit.surface,
            self.game.relative_x(0.91),
            self.game.relative_y(0.92),
        )

        def quit_click(game):
            game.running = False

        quit.click = quit_click

        self.texts = [title, back, quit]
        self.buttons = [back, quit]
    
    def draw(self, delta_time):
        """Draws MainMenu"""
        for text in self.texts:
            text.blit(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.color = (192, 192, 192)
                else:
                    button.color = (128, 128, 128)
                button.redraw()
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click(self.game)
        

