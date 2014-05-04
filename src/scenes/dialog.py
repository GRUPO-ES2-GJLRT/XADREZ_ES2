# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame
from .base import Scene
from .interfaces.dialog_interface import DialogInterface


class Dialog(Scene, DialogInterface):

    def __init__(self, chess, message, yes_click, no_click, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(Dialog, self).__init__(*args, **kwargs)
        self.chess = chess
        self.message = message
        self.yes_click = yes_click
        self.no_click = no_click
        self.define_clicks()
        self.create_interface()

    def define_clicks(self):

        def motion(it, collides):
            if collides:
                it.color = self.button_hover
            else:
                it.color = self.button_color
            it.redraw()
        self.motion = motion

    def draw(self):
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
        DialogInterface.resize(self)

    def close(self):
        self.chess.free_events()
        super(Dialog, self).close()
