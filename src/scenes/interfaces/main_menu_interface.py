# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame

from .interface import Interface
from scenes.elements import (
    GameDiv,
    GameTextElement,
)
from consts.i18n import (
    TITLE,
    AI_VS_AI,
    ONE_PLAYER,
    TWO_PLAYERS,
    CONFIG,
    QUIT,
)


class MainMenuInterface(Interface):

    def interface(self):
        title_font_size = lambda: self.game.relative_x(0.1)
        title_font = lambda: pygame.font.SysFont("", title_font_size())
        menu_font_size = lambda: self.game.relative_x(0.05)
        menu_font = lambda: pygame.font.SysFont("", menu_font_size())

        return GameDiv(name="main_div", children=[
            GameTextElement(
                name="title",
                font=title_font,
                text=TITLE,
                antialias=True,
                color=(192, 192, 192),
                x=lambda: self.game.center_x(),
                y=lambda: self.game.relative_y(0.1),
            ),
            GameTextElement(
                name="ai_vs_ai",
                font=menu_font,
                text=AI_VS_AI,
                antialias=True,
                color=(128, 128, 128),
                x=lambda: self.game.center_x(),
                y=lambda: (self.game.relative_y(0.45) - menu_font_size() // 2 -
                           self.game.relative_x(0.04)),
                click=self.ai_vs_ai_click,
                motion=self.motion,
            ),
            GameTextElement(
                name="one_player",
                font=menu_font,
                text=ONE_PLAYER,
                antialias=True,
                color=(128, 128, 128),
                x=lambda: self.game.center_x(),
                y=lambda: self.game.relative_y(0.45),
                click=self.one_player_click,
                motion=self.motion,
            ),
            GameTextElement(
                name="two_players",
                font=menu_font,
                text=TWO_PLAYERS,
                antialias=True,
                color=(128, 128, 128),
                x=lambda: self.game.center_x(),
                y=lambda: (self.game.relative_y(0.45) + menu_font_size() // 2 +
                           self.game.relative_x(0.04)),
                click=self.two_players_click,
                motion=self.motion,
            ),
            GameTextElement(
                name="configurations",
                font=menu_font,
                text=CONFIG,
                antialias=True,
                color=(128, 128, 128),
                x=lambda: self.game.relative_x(0.10),
                y=lambda: self.game.relative_y(0.92),
                click=self.configurations_click,
                motion=self.motion,
            ),
            GameTextElement(
                name="quit",
                font=menu_font,
                text=QUIT,
                antialias=True,
                color=(128, 128, 128),
                x=lambda: self.game.relative_x(0.91),
                y=lambda: self.game.relative_y(0.92),
                click=self.quit_click,
                motion=self.motion,
            ),
        ])

    def resize(self):
        self.main_div.call('redraw')
