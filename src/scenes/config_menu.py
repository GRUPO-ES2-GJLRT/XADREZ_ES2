# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

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
        self.timer = self.data['timer']

        # Fifty Move Rule
        self.fifty_move = self.data['fifty_move']

        # Jit Draw
        self.current_jit_draw = self.data['jit_draw']

        # Timeout
        self.timeout = self.data['timeout']

        # State
        self.show_moves = False
        self.show_bonus = False

        self.define_clicks()
        self.create_interface()
        self.update_labels_and_fields()

    def define_clicks(self):
        def back_click(it):
            self.save()
            self.game.scene = scenes.main_menu.MainMenu(self.game)

        def quit_click(it):
            self.close()

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

        def select_timer(it, option):
            self.timer = option
            self.update_labels_and_fields()

        def select_fiftymove(it, option):
            self.fifty_move = option

        def select_jit_draw(it, option):
            self.current_jit_draw = option

        def select_timeout(it, option):
            self.timeout = option

        def motion(it, collides, color):
            if collides:
                it.color = self.button_hover
            else:
                it.color = color()
            it.redraw()

        self.back_click = back_click
        self.quit_click = quit_click
        self.minutes_plus_click = partial(plus, element=lambda: self.minutes)
        self.moves_plus_click = partial(plus, element=lambda: self.moves)
        self.bonus_plus_click = partial(plus, element=lambda: self.bonus)
        self.minutes_minus_click = partial(minus, element=lambda: self.minutes)
        self.moves_minus_click = partial(minus, element=lambda: self.moves)
        self.bonus_minus_click = partial(minus, element=lambda: self.bonus)
        self.select_timer = select_timer
        self.select_fiftymove = select_fiftymove
        self.select_jit_draw = select_jit_draw
        self.select_timeout = select_timeout
        self.motion = partial(motion, color=lambda: self.button_color)
        self.motion_options = partial(motion, color=lambda: self.value_color)

    def update_labels_and_fields(self):
        self.show_bonus = False
        self.show_moves = False
        if self.timer == TIMER_OPTIONS["moves_per_minutes"]:
            self.show_moves = True
        elif self.timer == TIMER_OPTIONS["fischer_game"]:
            self.show_bonus = True

    def save(self):
        data = {
            'timer': self.timer,
            'minutes': int(self.minutes.value),
            'moves': int(self.moves.value),
            'bonus': int(self.bonus.value),
            'fifty_move': self.fifty_move,
            'jit_draw': self.current_jit_draw,
            'timeout': self.timeout
        }

        try:
            os.makedirs(os.path.abspath(self.data_dir))
        except:
            pass

        with open(os.path.abspath(os.path.join(self.data_dir, 'config.json')),
                  'w') as f:
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

    def resize(self):
        ConfigMenuInterface.resize(self)
