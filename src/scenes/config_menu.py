# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os
import json

from functools import partial

import scenes.main_menu

from scenes.base import Scene
from consts.default import TIMER_OPTIONS
from scenes.interfaces.config_menu_interface import ConfigMenuInterface

class ConfigMenu(Scene, ConfigMenuInterface):

    def __init__(self, *args, **kwargs):
        """ConfigMenu constructor. Creates texts and buttons"""
        super(ConfigMenu, self).__init__(*args, **kwargs)

        # Load current config
        self.data = self.load_stored_config()

        # Timer
        self.option = self.data['option']

        # State
        self.show_moves = False
        self.show_bonus = False

        # Load images
        ok = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, 'ok.png')))
        self.ok_image = pygame.transform.scale(ok, (50, 50))

        self.define_clicks()
        self.create_interface()
        self.update_labels_and_fields()

    def define_clicks(self):
        def back_click(it):
            self.save()
            self.game.scene = scenes.main_menu.MainMenu(self.game)

        def quit_click(it):
            self.game.running = False

        def plus(it, element):
            element = element()
            element.text = str(int(element.text) + 1)
            element.redraw()

        def minus(it, element):
            element = element()
            value = int(element.text)
            if value > 0:
                element.text = str(int(element.text) - 1)
                element.redraw()

        def set_option(it, option):
            self.option = TIMER_OPTIONS[option]
            self.update_labels_and_fields()

        def motion(it, collides):
            if collides:
                it.color = (192, 192, 192)
            else:
                it.color = (128, 128, 128)
            it.redraw()

        self.back_click = back_click
        self.quit_click = quit_click
        self.minutes_plus_click = partial(plus, element=lambda: self.minutes)
        self.moves_plus_click = partial(plus, element=lambda: self.moves)
        self.bonus_plus_click = partial(plus, element=lambda: self.bonus)
        self.minutes_minus_click = partial(minus, element=lambda: self.minutes)
        self.moves_minus_click = partial(minus, element=lambda: self.moves)
        self.bonus_minus_click = partial(minus, element=lambda: self.bonus)
        self.minutes_per_game_click = partial(set_option, option="minutes_per_game")
        self.moves_per_minutes_click = partial(set_option, option="moves_per_minutes")
        self.fischer_time_click = partial(set_option, option="fischer_game")
        self.motion = motion


    def update_labels_and_fields(self):
        self.show_bonus = False
        self.show_moves = False
        if self.option == TIMER_OPTIONS["minutes_per_game"]:
            self.ok.y = self.game.relative_y(0.26)
        elif self.option == TIMER_OPTIONS["moves_per_minutes"]:
            self.ok.y = self.game.relative_y(0.36)
            self.show_moves = True
        else:
            self.ok.y = self.game.relative_y(0.46)
            self.show_bonus = True
            self.show_bonus = (50, 360)

    def save(self):
        data = {
            'option': self.option,
            'minutes': int(self.minutes.text),
            'moves': int(self.moves.text),
            'bonus': int(self.bonus.text),
        }

        try:
            os.makedirs(os.path.abspath(self.data_dir))
        except:
            pass

        with open(os.path.abspath(os.path.join(self.data_dir, 'config.json')), 'w') as f:
            json.dump(data, f)

    def draw(self, delta_time):
        """Draws ConfigMenu"""
        self.main_div.draw(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            self.main_div.motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.main_div.click(event.pos)


