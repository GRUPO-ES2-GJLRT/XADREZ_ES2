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
        label_font = pygame.font.SysFont("", self.game.relative_x(0.04))

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

        #Minutes Field
        self.minutes = GameText(menu_font, "10", True, (192, 192, 192))
        self.minutes.rect = self.place_rect(
            self.minutes.surface,
            self.game.relative_x(0.85),
            self.game.relative_y(0.30),
        )

        # Number of moves Field
        self.moves = GameText(menu_font, "10", True, (192, 192, 192))
        self.moves.rect = self.place_rect(
            self.moves.surface,
            self.game.relative_x(0.85),
            self.game.relative_y(0.40),
        )

        # Bonus Field
        self.bonus = GameText(menu_font, "10", True, (192, 192, 192))
        self.bonus.rect = self.place_rect(
            self.bonus.surface,
            self.game.relative_x(0.85),
            self.game.relative_y(0.40),
        )

        #Label 1
        label_1 = GameText(label_font, "Minutes:", True, (96, 96, 96))
        label_1.rect = self.place_rect(
            label_1.surface,
            self.game.relative_x(0.72),
            self.game.relative_y(0.302),
        )

        #Label 2  Can be blank or "Moves", or "Bonus"
        label_2 = GameText(label_font, "", True, (96, 96, 96))
        label_2.rect = self.place_rect(
            label_2.surface,
            self.game.relative_x(0.665),
            self.game.relative_y(0.402),
        )

        # Plus Button 1
        plus_1 = GameText(menu_font, PLUS, True, (128, 128, 128))
        plus_1.rect = self.place_rect(
            plus_1.surface,
            self.game.relative_x(0.80),
            self.game.relative_y(0.30),
        )

        # Minus Button 1
        minus_1 = GameText(menu_font, MINUS, True, (128, 128, 128))
        minus_1.rect = self.place_rect(
            minus_1.surface,
            self.game.relative_x(0.90),
            self.game.relative_y(0.30),
        )

        # Plus Button 2
        plus_2 = GameText(menu_font, PLUS, True, (128, 128, 128))
        plus_2.rect = self.place_rect(
            plus_2.surface,
            self.game.relative_x(0.80),
            self.game.relative_y(0.40),
        )

        # Minus Button 2
        minus_2 = GameText(menu_font, MINUS, True, (128, 128, 128))
        minus_2.rect = self.place_rect(
            minus_2.surface,
            self.game.relative_x(0.90),
            self.game.relative_y(0.40),
        )

        def plus_1_click(game):
            self.minutes.text = str(int(self.minutes.text) + 1)
            self.minutes.redraw()

        def minus_1_click(game):
            minutes = int(self.minutes.text)
            if minutes > 0:
                self.minutes.text = str(int(minutes) - 1)
                self.minutes.redraw()

        def plus_2_click(game):
            if self.option == self.options["moves_per_minutes"]:
                self.moves.text = str(int(self.moves.text) + 1)
                self.moves.redraw()
            else:
                self.bonus.text = str(int(self.bonus.text) + 1)
                self.bonus.redraw()

        def minus_2_click(game):
            if self.option == self.options["moves_per_minutes"]:
                value = int(self.moves.text)
                if value > 0:
                    self.moves.text = str(int(self.moves.text) - 1)
                    self.moves.redraw()
            else:
                value = int(self.bonus.text)
                if value > 0:
                    self.bonus.text = str(int(self.bonus.text) - 1)
                    self.bonus.redraw()


        plus_1.click = plus_1_click
        minus_1.click = minus_1_click
        plus_2.click = plus_2_click
        minus_2.click = minus_2_click

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
            update_labels_and_fields()

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
            update_labels_and_fields()

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
            update_labels_and_fields()

        fischer_time.click = fischer_time_click;

        # Quit Button
        quit = GameText(menu_font, QUIT, True, (128, 128, 128))
        quit.rect = self.place_rect(
            quit.surface,
            self.game.relative_x(0.91),
            self.game.relative_y(0.92),
        )

        #The options will change when the game mode change
        def update_labels_and_fields():
            if self.option == self.options["minutes_per_game"]:
                label_2.text = ""
                label_2.redraw()
                if self.moves in self.texts:
                    self.texts.remove(self.moves)
                if self.bonus in self.texts:
                    self.texts.remove(self.bonus)
                if plus_2 in self.texts:
                    self.texts.remove(plus_2)
                    self.texts.remove(minus_2)
                    self.buttons.remove(plus_2)
                    self.buttons.remove(minus_2)
            elif self.option == self.options["moves_per_minutes"]:
                label_2.text = MOVES_LABEL
                label_2.redraw()
                if self.moves not in self.texts:
                    self.texts.append(self.moves)
                if self.bonus in self.texts:
                    self.texts.remove(self.bonus)
                if plus_2 not in self.texts:
                    self.texts.extend((plus_2, minus_2))
                    self.buttons.extend((plus_2, minus_2))
            else:
                label_2.text = BONUS_LABEL
                label_2.redraw()
                if self.bonus not in self.texts:
                    self.texts.append(self.bonus)
                if self.moves in self.texts:
                    self.texts.remove(self.moves)
                if plus_2 not in self.texts:
                    self.texts.extend((plus_2, minus_2))
                    self.buttons.extend((plus_2, minus_2))

        def quit_click(game):
            game.running = False

        quit.click = quit_click

        self.texts = [title, back, quit, minutes_per_game, moves_per_minutes, fischer_time, self.minutes, plus_1, minus_1, label_1, label_2]
        self.buttons = [back, quit, minutes_per_game, moves_per_minutes, fischer_time, plus_1, minus_1]
    
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
        

