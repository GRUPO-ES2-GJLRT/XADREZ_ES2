# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .menu_interface import MenuInterface

from scenes.elements import (
    GameDiv,
    GameTextElement,
    ButtonGroup,
)
from consts.i18n import (
    YES, NO
)


class DialogInterface(MenuInterface):

    def interface(self):
        MenuInterface.interface(self)

        return GameDiv(name="main_div", children=[
            ButtonGroup(
                color=(0, 0, 0, 128),
                radius=0,
                define_rect=lambda: [0,
                                     0,
                                     self.game.width,
                                     self.game.height],
            ),
            ButtonGroup(
                color=self.main_menu_color,
                padding=10,
                children=[
                    GameTextElement(
                        font=self.menu_font,
                        text=self.message,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) -
                                   self.menu_font.size // 2 -
                                   self.game.relative_x(0.04)),
                    ),
                    GameTextElement(
                        name="yes",
                        font=self.menu_font,
                        text=YES,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: self.game.relative_y(0.45),
                        click=self.yes_click,
                        motion=self.motion,
                    ),
                    GameTextElement(
                        name="no",
                        font=self.menu_font,
                        text=NO,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.center_x(),
                        y=lambda: (self.game.relative_y(0.45) +
                                   self.menu_font.size // 2 +
                                   self.game.relative_x(0.04)),
                        click=self.no_click,
                        motion=self.motion,
                    ),
                ]
            ),
        ])
