# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame
import scenes
from .base import Scene
from .interfaces.pause_menu_interface import PauseMenuInterface


class PauseMenu(Scene, PauseMenuInterface):

    def __init__(self, chess, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(PauseMenu, self).__init__(*args, **kwargs)
        self.chess = chess
        self.define_clicks()
        self.create_interface()

    def define_clicks(self):
        def resume_click(it):
            self.chess.resume()

        def restart_click(it):
            self.chess.new_game()

        def exit_click(it):
            self.chess.free_events()
            self.game.scene = scenes.main_menu.MainMenu(self.game)

        def quit_click(it):
            self.close()

        def motion(it, collides):
            if collides:
                it.color = self.button_hover
            else:
                it.color = self.button_color
            it.redraw()

        self.resume_click = resume_click
        self.restart_click = restart_click
        self.exit_click = exit_click
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resume_click(self)

    def resize(self):
        PauseMenuInterface.resize(self)

    def close(self):
        self.chess.free_events()
        super(PauseMenu, self).close()
