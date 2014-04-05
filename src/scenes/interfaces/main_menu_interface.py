# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .menu_interface import MenuInterface

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


class MainMenuInterface(MenuInterface):

    def interface(self):
        MenuInterface.interface(self)

        return GameDiv(name="main_div", children=[
            ImageElement(
                image=self.background_image
            ),
            GameTextElement(
                name="title",
                font=self.title_font,
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
                        font=self.menu_font,
                        text=AI_VS_AI,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) -
                                   self.menu_font.size // 2 -
                                   self.game.relative_x(0.04)),
                        click=self.ai_vs_ai_click,
                        motion=self.motion,
                    ),
                    GameTextElement(
                        name="one_player",
                        font=self.menu_font,
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
                        font=self.menu_font,
                        text=TWO_PLAYERS,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) +
                                   self.menu_font.size // 2 +
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
                        font=self.menu_font,
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
                        font=self.menu_font,
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
