# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
from consts.i18n import *

from .base import Scene, GameText
from .chess import Chess
from .config_menu import ConfigMenu
from .interfaces.main_menu_interface import MainMenuInterface

class MainMenu(Scene, MainMenuInterface):

    def __init__(self, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(MainMenu, self).__init__(*args, **kwargs)
        self.define_clicks()
        self.create_interface()

    def define_clicks(self):
        def one_player_click(it):
            self.game.scene = Chess(game=self.game, one_player=True, selected_level=0) 

        def two_players_click(it):
            self.game.scene = Chess(game=self.game, one_player=False, selected_level=None) 

        def configurations_click(it):
            self.game.scene = ConfigMenu(self.game)

        def quit_click(it):
            self.game.running = False

        def motion(it, collides):
            if collides:
                it.color = (192, 192, 192)
            else:
                it.color = (128, 128, 128)
            it.redraw()

        self.one_player_click = one_player_click
        self.two_players_click = two_players_click
        self.configurations_click = configurations_click
        self.quit_click = quit_click
        self.motion = motion

    def draw(self, delta_time):
        """Draws MainMenu"""
        self.main_div.draw(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            self.main_div.motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.main_div.click(event.pos)

