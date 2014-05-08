# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from functools import partial
from collections import OrderedDict

import pygame

from .base import Scene
from .chess import Chess
from .config_menu import ConfigMenu
from .interfaces.main_menu_interface import MainMenuInterface
from consts.i18n import (
    PLAYER_LABEL,
    SOOO_EASY_LABEL,
    EASY_LABEL,
    MEDIUM_LABEL,
    HARD_LABEL
)

from game_elements.ai_player import (
    PLAYER,
    SOOO_EASY,
    EASY,
    MEDIUM,
    HARD
)


class MainMenu(Scene, MainMenuInterface):

    def __init__(self, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(MainMenu, self).__init__(*args, **kwargs)
        self.players = OrderedDict([
            (PLAYER, PLAYER_LABEL),
            (SOOO_EASY, SOOO_EASY_LABEL),
            (EASY, EASY_LABEL),
            (MEDIUM, MEDIUM_LABEL),
            (HARD, HARD_LABEL),
        ])
        self.white_player = None
        self.black_player = MEDIUM

        self.define_clicks()
        self.create_interface()

    def define_clicks(self):
        def play_click(it):
            self.game.scene = Chess(
                game=self.game,
                level_white=self.select_white.current,
                level_black=self.select_black.current
            )

        def configurations_click(it):
            self.game.scene = ConfigMenu(self.game)

        def quit_click(it):
            self.close()

        def motion(it, collides, color):
            if collides:
                it.color = self.button_hover
            else:
                it.color = color()
            it.redraw()

        self.play_click = play_click
        self.configurations_click = configurations_click
        self.quit_click = quit_click
        self.motion = partial(motion, color=lambda: self.button_color)
        self.white_motion = partial(motion, color=lambda: (255, 255, 255))
        self.black_motion = partial(motion, color=lambda: (0, 0, 0))

    def draw(self, delta_time):
        """Draws MainMenu"""
        self.main_div.draw(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            self.main_div.motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.main_div.click(event.pos)

    def resize(self):
        MainMenuInterface.resize(self)
