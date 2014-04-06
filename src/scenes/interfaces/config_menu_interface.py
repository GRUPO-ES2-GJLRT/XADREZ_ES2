# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .menu_interface import MenuInterface

from scenes.elements import (
    GameDiv,
    ImageElement,
    GameTextElement,
    ButtonGroup,
    ListOptionElement,
)
from consts.i18n import (
    CONFIG,
    BACK,
    QUIT,
    MINUTES_LABEL,
    MOVES_LABEL,
    BONUS_LABEL,
    PLUS,
    MINUS,
    MINUTES_PER_GAME,
    MOVES_PER_MINUTES,
    FISCHER_TIME,
    TIMER_LABEL,
    FIFTY_MOVE_LABEL,
    FIFTY_MOVE_AUTO,
    FIFTY_MOVE_BUTTON,
    FIFTY_MOVE_DISABLE,
)
from consts.default import TIMER_OPTIONS, FIFTY_MOVE_OPTIONS


class ConfigMenuInterface(MenuInterface):

    def interface(self):
        MenuInterface.interface(self)

        return GameDiv(name="main_div", children=[
            ImageElement(
                image=self.background_image
            ),
            GameTextElement(
                name="title",
                font=self.title_font,
                text=CONFIG,
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
                define_rect=lambda: [self.game.relative_x(0.03),
                                     self.game.relative_y(0.25),
                                     self.game.relative_x(0.94),
                                     self.game.relative_y(0.60)],
            ),
            ButtonGroup(
                color=self.button_background,
                padding=5,
                radius=0.3,
                children=[
                    GameTextElement(
                        name="back",
                        font=self.menu_font,
                        text=BACK,
                        antialias=True,
                        color=self.button_color,
                        x=lambda: self.game.relative_x(0.10),
                        y=lambda: self.game.relative_y(0.92),
                        click=self.back_click,
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
            GameDiv(
                name="options",
                x=lambda: self.game.relative_x(0.80),
                children=[
                    GameDiv(
                        x=lambda: self.game.relative_x(0.05),
                        children=[
                            GameTextElement(
                                name="minutes",
                                font=self.menu_font,
                                text=str(self.data['minutes']),
                                antialias=True,
                                color=self.value_color,
                                y=lambda: self.game.relative_y(0.30),
                            ),
                            GameTextElement(
                                name="moves",
                                font=self.menu_font,
                                text=str(self.data['moves']),
                                antialias=True,
                                color=self.value_color,
                                y=lambda: self.game.relative_y(0.40),
                                condition=lambda: self.show_moves
                            ),
                            GameTextElement(
                                name="bonus",
                                font=self.menu_font,
                                text=str(self.data['bonus']),
                                antialias=True,
                                color=self.value_color,
                                y=lambda: self.game.relative_y(0.40),
                                condition=lambda: self.show_bonus
                            ),
                        ]
                    ),
                    GameDiv(
                        name="labels",
                        children=[
                            GameTextElement(
                                font=self.label_font,
                                text=MINUTES_LABEL,
                                antialias=True,
                                color=self.button_color,
                                x=lambda: -self.game.relative_x(0.08),
                                y=lambda: self.game.relative_y(0.302),
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=MOVES_LABEL,
                                antialias=True,
                                color=self.button_color,
                                x=lambda: -self.game.relative_x(0.08),
                                y=lambda: self.game.relative_y(0.402),
                                condition=lambda: self.show_moves
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=BONUS_LABEL,
                                antialias=True,
                                color=self.button_color,
                                x=lambda: -self.game.relative_x(0.08),
                                y=lambda: self.game.relative_y(0.402),
                                condition=lambda: self.show_bonus
                            ),
                        ]
                    ),
                    GameDiv(
                        name="plus",
                        x=lambda: self.game.relative_x(0.1),
                        children=[
                            GameTextElement(
                                font=self.label_font,
                                text=PLUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.30),
                                motion=self.motion,
                                click=self.minutes_plus_click,
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=PLUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.40),
                                motion=self.motion,
                                click=self.moves_plus_click,
                                condition=lambda: self.show_moves
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=PLUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.40),
                                motion=self.motion,
                                click=self.bonus_plus_click,
                                condition=lambda: self.show_bonus
                            ),
                        ]
                    ),
                    GameDiv(
                        name="minus",
                        x=lambda: self.game.relative_x(0),
                        children=[
                            GameTextElement(
                                font=self.label_font,
                                text=MINUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.30),
                                motion=self.motion,
                                click=self.minutes_minus_click,
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=MINUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.40),
                                motion=self.motion,
                                click=self.moves_minus_click,
                                condition=lambda: self.show_moves
                            ),
                            GameTextElement(
                                font=self.label_font,
                                text=MINUS,
                                antialias=True,
                                color=self.button_color,
                                y=lambda: self.game.relative_y(0.40),
                                motion=self.motion,
                                click=self.bonus_minus_click,
                                condition=lambda: self.show_bonus
                            ),
                        ]
                    ),
                ]
            ),
            ListOptionElement(
                font=self.label_font,
                label=TIMER_LABEL,
                antialias=True,
                label_color=self.button_color,
                option_color=self.value_color,
                current=self.timer,
                x=lambda: self.game.relative_x(0.12),
                y=lambda: self.game.relative_y(0.28),
                options={
                    TIMER_OPTIONS["minutes_per_game"]: MINUTES_PER_GAME,
                    TIMER_OPTIONS["moves_per_minutes"]: MOVES_PER_MINUTES,
                    TIMER_OPTIONS["fischer_game"]: FISCHER_TIME,
                },
                motion=self.motion_options,
                select=self.select_timer,
            ),
            ListOptionElement(
                font=self.label_font,
                label=FIFTY_MOVE_LABEL,
                antialias=True,
                label_color=self.button_color,
                option_color=self.value_color,
                current=self.fifty_move,
                x=lambda: self.game.relative_x(0.12),
                y=lambda: self.game.relative_y(0.38),
                options={
                    FIFTY_MOVE_OPTIONS["auto"]: FIFTY_MOVE_AUTO,
                    FIFTY_MOVE_OPTIONS["button"]: FIFTY_MOVE_BUTTON,
                    FIFTY_MOVE_OPTIONS["disable"]: FIFTY_MOVE_DISABLE,
                },
                motion=self.motion_options,
                select=self.select_fiftymove,
            ),
        ])
