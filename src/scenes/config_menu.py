# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame, os

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


        # Options
        self.options = {"minutes_per_game": 1, "moves_per_minutes": 2, "fischer_game": 3}
        self.option = self.options["minutes_per_game"]

        #Ok Image
        self.ok_position = (50, 200)
        ok = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, 'ok.png')))
        self.ok = pygame.transform.scale(ok, (50, 50))

        self.minutes = GameText(menu_font, "10", True, (192, 192, 192))
        self.minutes.rect = self.place_rect(
            self.minutes.surface,
            self.game.relative_x(0.85),
            self.game.relative_y(0.30),
        )

        # Plus Button
        plus = GameText(menu_font, PLUS, True, (128, 128, 128))
        plus.rect = self.place_rect(
            plus.surface,
            self.game.relative_x(0.80),
            self.game.relative_y(0.30),
        )

        # Minus Button
        minus = GameText(menu_font, MINUS, True, (128, 128, 128))
        minus.rect = self.place_rect(
            minus.surface,
            self.game.relative_x(0.90),
            self.game.relative_y(0.30),
        )

        def plus_click(game):
            self.minutes.text = str(int(self.minutes.text) + 1)

        def minus_click(game):
            self.minutes.text = str(int(self.minutes.text) - 1)

        plus.click = plus_click
        minus.click = minus_click

        # Minutes_per_Game Button
        minutes_per_game = GameText(menu_font, MINUTES_PER_GAME, True, (128, 128, 128))
        minutes_per_game.rect = self.place_rect(
            minutes_per_game.surface,
            self.game.relative_x(0.30),
            self.game.relative_y(0.30),
        )

        def minutes_per_game_click(game):
            self.ok_position = (50, 200)
            self.option = self.options["minutes_per_game"]

        minutes_per_game.click = minutes_per_game_click;

        # Moves_per_Minutes Button
        moves_per_minutes = GameText(menu_font, MOVES_PER_MINUTES, True, (128, 128, 128))
        moves_per_minutes.rect = self.place_rect(
            moves_per_minutes.surface,
            self.game.relative_x(0.30),
            self.game.relative_y(0.40),
        )

        def moves_per_minutes_click(game):
            self.ok_position = (50, 280)
            self.option = self.options["moves_per_minutes"]

        moves_per_minutes.click = moves_per_minutes_click;

        # Fischer_Time Button
        fischer_time = GameText(menu_font, FISCHER_TIME, True, (128, 128, 128))
        fischer_time.rect = self.place_rect(
            fischer_time.surface,
            self.game.relative_x(0.30),
            self.game.relative_y(0.50),
        )

        def fischer_time_click(game):
            self.ok_position = (50, 360)
            self.option = self.options["fischer_game"]

        fischer_time.click = fischer_time_click;

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

        self.texts = [title, back, quit, minutes_per_game, moves_per_minutes, fischer_time, self.minutes, plus, minus]
        self.buttons = [back, quit, minutes_per_game, moves_per_minutes, fischer_time, plus, minus]
    
    def draw(self, delta_time):
        """Draws MainMenu"""
        for text in self.texts:
            text.blit(self.game.screen)
        self.game.screen.blit(self.ok, self.ok_position)


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
        

