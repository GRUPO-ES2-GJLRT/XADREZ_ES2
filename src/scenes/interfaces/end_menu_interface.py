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
    RESTART,
    EXIT,
    DRAW_MESSAGE,
    BLACK_WINS_MESSAGE,
    WHITE_WINS_MESSAGE
)
import scenes.chess


class EndMenuInterface(MenuInterface):

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
            GameDiv(
                x=lambda: self.game.center_x(),
                y=lambda: self.game.relative_y(0.15),
                children=[
                    GameTextElement(
                        font=self.title_font,
                        text=DRAW_MESSAGE,
                        antialias=True,
                        color=(30, 144, 255),
                        style="outline",
                        other_color=(255, 255, 255),
                        condition=(lambda: self.chess.state ==
                                   scenes.chess.GAME_DRAW)
                    ),
                    GameTextElement(
                        font=self.title_font,
                        text=BLACK_WINS_MESSAGE,
                        antialias=True,
                        color=(50, 50, 50),
                        style="outline",
                        other_color=(255, 255, 255),
                        condition=(lambda: self.chess.state ==
                                   scenes.chess.BLACK_WINS)
                    ),
                    GameTextElement(
                        font=self.title_font,
                        text=WHITE_WINS_MESSAGE,
                        antialias=True,
                        color=(255, 255, 255),
                        style="outline",
                        other_color=(50, 50, 50),
                        condition=(lambda: self.chess.state ==
                                   scenes.chess.WHITE_WINS)
                    ),
                ]
            ),
            ButtonGroup(
                color=self.main_menu_color,
                padding=10,
                children=[
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
        ])
