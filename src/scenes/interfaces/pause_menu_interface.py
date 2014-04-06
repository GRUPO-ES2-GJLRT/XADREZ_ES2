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
    PAUSE,
    RESUME,
    RESTART,
    EXIT,
    QUIT,
)


class PauseMenuInterface(MenuInterface):

    def interface(self):
        MenuInterface.interface(self)

        return GameDiv(name="main_div", children=[
            ImageElement(
                image=self.background_image
            ),
            GameTextElement(
                name="title",
                font=self.title_font,
                text=PAUSE,
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
                        name="resume",
                        font=self.menu_font,
                        text=RESUME,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) -
                                   self.menu_font.size // 2 -
                                   self.game.relative_x(0.04)),
                        click=self.resume_click,
                        motion=self.motion,
                    ),
                    GameTextElement(
                        name="restart",
                        font=self.menu_font,
                        text=RESTART,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: self.game.relative_y(0.45),
                        click=self.restart_click,
                        motion=self.motion,
                    ),
                    GameTextElement(
                        name="exit",
                        font=self.menu_font,
                        text=EXIT,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) +
                                   self.menu_font.size // 2 +
                                   self.game.relative_x(0.04)),
                        click=self.exit_click,
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
            ),
        ])
