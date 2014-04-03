# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame

from os import path

from .interface import Interface
from scenes.elements import (
    GameDiv,
    GameTextElement,
    ImageElement,
    ButtonGroup,
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
        self.button_color = (255, 255, 255)
        self.button_hover = (200, 200, 200)
        self.title_color = (200, 150, 0)
        self.title_outline = (255, 222, 173)
        self.main_menu_color = (175, 125, 0, 150)
        self.button_background = (175, 125, 0, 200)
        title_font_size = lambda: self.game.relative_x(0.15)
        title_font = lambda: pygame.font.SysFont("", title_font_size())
        menu_font_size = lambda: self.game.relative_x(0.05)
        menu_font = lambda: pygame.font.SysFont("", menu_font_size())
        self.load_images()

        return GameDiv(name="main_div", children=[
            ImageElement(
                image=lambda: self.background_image
            ),
            GameTextElement(
                name="title",
                font=title_font,
                text=TITLE,
                antialias=True,
                color=self.title_color,
                style="outline",
                other_color=self.title_outline,
                x=lambda: self.game.center_x(),
                y=lambda: self.game.relative_y(0.15),
            ),
            ButtonGroup(
                color=self.main_menu_color,
                padding=10,
                children=[
                    GameTextElement(
                        name="ai_vs_ai",
                        font=menu_font,
                        text=AI_VS_AI,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) -
                                   menu_font_size() // 2 -
                                   self.game.relative_x(0.04)),
                        click=self.ai_vs_ai_click,
                        motion=self.motion,
                    ),
                    GameTextElement(
                        name="one_player",
                        font=menu_font,
                        text=ONE_PLAYER,
                        antialias=True,
                        color=self.button_color,
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
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) +
                                   menu_font_size() // 2 +
                                   self.game.relative_x(0.04)),
                        click=self.two_players_click,
                        motion=self.motion,
                    ),
                ]
            ),
            ButtonGroup(
                color=self.button_background,
                padding=5,
                radius=0.3,
                children=[
                    GameTextElement(
                        name="configurations",
                        font=menu_font,
                        text=CONFIG,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.relative_x(0.10),
                        y=lambda: self.game.relative_y(0.92),
                        click=self.configurations_click,
                        motion=self.motion,
                    ),
                ]
            ),
            ButtonGroup(
                color=self.button_background,
                padding=5,
                radius=0.3,
                children=[
                    GameTextElement(
                        name="quit",
                        font=menu_font,
                        text=QUIT,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.relative_x(0.91),
                        y=lambda: self.game.relative_y(0.92),
                        click=self.quit_click,
                        motion=self.motion,
                    ),
                ]
            )
        ])

    def load_images(self):
        self.background_original = pygame.image.load(
            path.join(self.assets_dir, 'background.jpg'))

        self.transform_images()

    def transform_images(self):
        self.background_image = pygame.transform.scale(
            self.background_original,
            (self.game.width, self.game.height)
        )

    def resize(self):
        self.main_div.call('redraw')
        self.transform_images()
