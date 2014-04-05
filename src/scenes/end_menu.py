# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame
import scenes
from .base import Scene
from .interfaces.end_menu_interface import EndMenuInterface


class EndMenu(Scene, EndMenuInterface):

    def __init__(self, chess, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(EndMenu, self).__init__(*args, **kwargs)
        self.chess = chess
        self.define_clicks()
        self.create_interface()

    def define_clicks(self):

        def restart_click(it):
            self.chess.new_game()

        def exit_click(it):
            self.chess.free_events()
            self.game.scene = scenes.main_menu.MainMenu(self.game)

        def motion(it, collides):
            if collides:
                it.color = self.button_hover
            else:
                it.color = self.button_color
            it.redraw()

        self.restart_click = restart_click
        self.exit_click = exit_click
        self.motion = motion

    def draw(self, delta_time):
        """Draws MainMenu"""
        self.game.screen.fill((238, 223, 204))
        self.chess.main_div.draw(self.game.screen)
        self.main_div.draw(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            self.main_div.motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.main_div.click(event.pos)

    def resize(self):
        self.chess.resize()
        EndMenuInterface.resize(self)
