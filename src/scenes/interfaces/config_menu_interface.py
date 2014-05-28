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
    NumberOptionElement,
)
from consts.i18n import (
    CONFIG,
    BACK,
    QUIT,
    MINUTES_LABEL,
    MOVES_LABEL,
    BONUS_LABEL,
    MINUTES_PER_GAME,
    MOVES_PER_MINUTES,
    FISCHER_TIME,
    TIMER_LABEL,
    FIFTY_MOVE_LABEL,
    FIFTY_MOVE_AUTO,
    FIFTY_MOVE_BUTTON,
    FIFTY_MOVE_DISABLE,
    JIT_DRAW_LABEL,
    JIT_DRAW_ENABLE,
    JIT_DRAW_DISABLE,
    TIMEOUT_LABEL,
    TIMEOUT_1S,
    TIMEOUT_2S,
    TIMEOUT_3S,
    TIMEOUT_5S,
    TIMEOUT_8S,
    TIMEOUT_13S,
    TIMEOUT_21S,
    TIMEOUT_34S,
)
from consts.default import (
    TIMER_OPTIONS, 
    FIFTY_MOVE_OPTIONS, 
    JIT_DRAW_OPTIONS,
    TIMEOUT_OPTIONS,
)


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
                x=lambda: self.game.relative_x(0.66),
                children=[
                    NumberOptionElement(
                        name="minutes",
                        font=self.label_font,
                        label=MINUTES_LABEL,
                        antialias=True,
                        label_color=self.button_color,
                        option_color=self.value_color,
                        y=lambda: self.game.relative_y(0.28),
                        current=self.data['minutes'],
                        motion=self.motion,
                    ),
                    NumberOptionElement(
                        name="moves",
                        font=self.label_font,
                        label=MOVES_LABEL,
                        antialias=True,
                        label_color=self.button_color,
                        option_color=self.value_color,
                        y=lambda: self.game.relative_y(0.38),
                        current=self.data['moves'],
                        motion=self.motion,
                        condition=lambda: self.show_moves
                    ),
                    NumberOptionElement(
                        name="bonus",
                        font=self.label_font,
                        label=BONUS_LABEL,
                        antialias=True,
                        label_color=self.button_color,
                        option_color=self.value_color,
                        y=lambda: self.game.relative_y(0.38),
                        current=self.data['bonus'],
                        motion=self.motion,
                        condition=lambda: self.show_bonus
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
            ListOptionElement(
                font=self.label_font,
                label=JIT_DRAW_LABEL,
                antialias=True,
                label_color=self.button_color,
                option_color=self.value_color,
                current=self.current_jit_draw,
                x=lambda: self.game.relative_x(0.12),
                y=lambda: self.game.relative_y(0.48),
                options={
                    JIT_DRAW_OPTIONS["enable"]: JIT_DRAW_ENABLE,
                    JIT_DRAW_OPTIONS["disable"]: JIT_DRAW_DISABLE,
                },
                motion=self.motion_options,
                select=self.select_jit_draw,
            ),
            ListOptionElement(
                font=self.label_font,
                label=TIMEOUT_LABEL,
                antialias=True,
                label_color=self.button_color,
                option_color=self.value_color,
                current=self.timeout,
                x=lambda: self.game.relative_x(0.12),
                y=lambda: self.game.relative_y(0.58),
                options={
                    TIMEOUT_OPTIONS["1s"]: TIMEOUT_1S,
                    TIMEOUT_OPTIONS["2s"]: TIMEOUT_2S,
                    TIMEOUT_OPTIONS["3s"]: TIMEOUT_3S,
                    TIMEOUT_OPTIONS["5s"]: TIMEOUT_5S,
                    TIMEOUT_OPTIONS["8s"]: TIMEOUT_8S,
                    TIMEOUT_OPTIONS["13s"]: TIMEOUT_13S,
                    TIMEOUT_OPTIONS["21s"]: TIMEOUT_21S,
                    TIMEOUT_OPTIONS["34s"]: TIMEOUT_34S,
                },
                motion=self.motion_options,
                select=self.select_timeout,
            ),
        ])
