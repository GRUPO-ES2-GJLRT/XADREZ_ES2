# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame, os, json

from .base import Scene, GameText
from consts.i18n import *
from consts.default import TIMER_OPTIONS, TIMER, MINUTES, MOVES, BONUS


class ConfigMenu(Scene):

    def __init__(self, *args, **kwargs):
        """ConfigMenu constructor. Creates texts and buttons"""
        super(ConfigMenu, self).__init__(*args, **kwargs)


        # Load current config
        data = self.load_stored_config()

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
        self.set_text_position(back, 0.10, 0.92)

        def back_click(game):
            from .main_menu import MainMenu
            self.save()
            game.scene = MainMenu(game)

        back.click = back_click

    
        # Timer
        self.option = data['option']

        #Ok Image
        self.ok_position = (50, 200)
        ok = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, 'ok.png')))
        self.ok = pygame.transform.scale(ok, (50, 50))

        #Minutes Field
        self.minutes = GameText(menu_font, str(data['minutes']), True, (192, 192, 192))
        self.set_text_position(self.minutes, 0.85, 0.30)

        # Number of moves Field
        self.moves = GameText(menu_font, str(data['moves']), True, (192, 192, 192))
        self.set_text_position(self.moves, 0.85, 0.40)

        # Bonus Field
        self.bonus = GameText(menu_font, str(data['bonus']), True, (192, 192, 192))
        self.set_text_position(self.bonus, 0.85, 0.40)

        #Label 1
        label_1 = GameText(label_font, "Minutes:", True, (96, 96, 96))
        self.set_text_position(label_1, 0.72, 0.302)

        #Label 2  Can be blank or "Moves", or "Bonus"
        label_2 = GameText(label_font, "", True, (96, 96, 96))
        self.set_text_position(label_2, 0.665, 0.402)

        # Plus Button 1
        plus_1 = GameText(menu_font, PLUS, True, (128, 128, 128))
        self.set_text_position(plus_1, 0.80, 0.30)

        # Minus Button 1
        minus_1 = GameText(menu_font, MINUS, True, (128, 128, 128))
        self.set_text_position(minus_1, 0.90, 0.30)

        # Plus Button 2
        plus_2 = GameText(menu_font, PLUS, True, (128, 128, 128))
        self.set_text_position(plus_2, 0.80, 0.40)

        # Minus Button 2
        minus_2 = GameText(menu_font, MINUS, True, (128, 128, 128))
        self.set_text_position(minus_2, 0.90, 0.40)

        def plus_1_click(game):
            self.minutes.text = str(int(self.minutes.text) + 1)
            self.minutes.redraw()

        def minus_1_click(game):
            minutes = int(self.minutes.text)
            if minutes > 0:
                self.minutes.text = str(int(self.minutes.text) - 1)
                self.minutes.redraw()

        def plus_2_click(game):
            if self.option == TIMER_OPTIONS["moves_per_minutes"]:
                self.moves.text = str(int(self.moves.text) + 1)
                self.moves.redraw()
            else:
                self.bonus.text = str(int(self.bonus.text) + 1)
                self.bonus.redraw()

        def minus_2_click(game):
            if self.option == TIMER_OPTIONS["moves_per_minutes"]:
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
        self.set_text_position(minutes_per_game, 0.30, 0.30)

        def minutes_per_game_click(game):
            self.option = TIMER_OPTIONS["minutes_per_game"]
            update_labels_and_fields()

        minutes_per_game.click = minutes_per_game_click;

        # Moves_per_Minutes Button
        moves_per_minutes = GameText(menu_font, MOVES_PER_MINUTES, True, (128, 128, 128))
        self.set_text_position(moves_per_minutes, 0.30, 0.40)

        def moves_per_minutes_click(game):
            self.option = TIMER_OPTIONS["moves_per_minutes"]
            update_labels_and_fields()

        moves_per_minutes.click = moves_per_minutes_click;

        # Fischer_Time Button
        fischer_time = GameText(menu_font, FISCHER_TIME, True, (128, 128, 128))
        self.set_text_position(fischer_time, 0.30, 0.50)

        def fischer_time_click(game):
            self.option = TIMER_OPTIONS["fischer_game"]
            update_labels_and_fields()

        fischer_time.click = fischer_time_click;

        # Quit Button
        quit = GameText(menu_font, QUIT, True, (128, 128, 128))
        self.set_text_position(quit, 0.91, 0.92)

        def quit_click(game):
            game.running = False

        quit.click = quit_click

        default_texts = [title, back, quit, minutes_per_game, moves_per_minutes, fischer_time, self.minutes, plus_1, minus_1, label_1, label_2]
        default_buttons =  [back, quit, minutes_per_game, moves_per_minutes, fischer_time, plus_1, minus_1]
        
        #The options will change when the game mode change
        def update_labels_and_fields():
            extra_texts = []
            extra_buttons = []
            if self.option == TIMER_OPTIONS["minutes_per_game"]:
                self.ok_position = (50, 200)
                label_2.text = ""
            elif self.option == TIMER_OPTIONS["moves_per_minutes"]:
                self.ok_position = (50, 280)
                label_2.text = MOVES_LABEL
                extra_texts = [self.moves, plus_2, minus_2]
                extra_buttons = [plus_2, minus_2]
            else:
                self.ok_position = (50, 360)
                label_2.text = BONUS_LABEL  
                extra_texts = [self.bonus, plus_2, minus_2]
                extra_buttons = [plus_2, minus_2]
            label_2.redraw()
            self.texts = default_texts + extra_texts 
            self.buttons = default_buttons + extra_buttons

        self.texts = default_texts
        self.buttons = default_buttons

        update_labels_and_fields()
    

    def save(self):
        data = {
            'option': self.option,
            'minutes': int(self.minutes.text),
            'moves': int(self.moves.text),
            'bonus': int(self.bonus.text),
        }
        with open(os.path.abspath(os.path.join(self.data_dir, 'config.json')), 'w') as f:
            json.dump(data, f)
        

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
        

