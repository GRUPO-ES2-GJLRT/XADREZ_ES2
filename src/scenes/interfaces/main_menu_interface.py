# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .menu_interface import MenuInterface

from scenes.elements import (
    GameDiv,
    GameTextElement,
    ImageElement,
    ButtonGroup,
    ListOptionElement
)
from consts.i18n import (
    TITLE,
    PLAY,
    WHITE_LABEL,
    BLACK_LABEL,
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
                        name="play",
                        font=self.menu_font,
                        text=PLAY,
                        antialias=True,
                        color=self.value_color,
                        top=True,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) -
                                   self.menu_font.size // 2 -
                                   self.game.relative_x(0.04)),
                        click=self.play_click,
                        motion=self.motion,
                    ),
                    ListOptionElement(
                        name='select_white',
                        font=self.menu_font,
                        label=WHITE_LABEL,
                        antialias=True,
                        label_color=(255, 255, 255),
                        option_color=(255, 255, 255),
                        current=self.white_player,
                        x=lambda: (self.game.center_x() -
                                   self.select_white.width() // 2),
                        y=lambda: (self.game.relative_y(0.45)),
                        options=self.players,
                        motion=self.white_motion,
                    ),
                    ListOptionElement(
                        name='select_black',
                        font=self.menu_font,
                        label=BLACK_LABEL,
                        antialias=True,
                        label_color=(0, 0, 0),
                        option_color=(0, 0, 0),
                        current=self.black_player,
                        x=lambda: (self.game.center_x() -
                                   self.select_black.width() // 2),
                        y=lambda: (self.game.relative_y(0.45) +
                                   self.menu_font.size),
                        options=self.players,
                        motion=self.black_motion,
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
