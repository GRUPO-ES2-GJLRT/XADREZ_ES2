import pygame
from .interface import Interface
from .elements import (
    GameDiv, 
    ImageElement, 
    RectElement,
    GameTextElement, 
    PiecesElement, 
    SquareElement,
)

from consts.i18n import *

class ConfigMenuInterface(Interface):

    def interface(self):
        title_font = pygame.font.SysFont("", self.game.relative_x(0.1))
        menu_font_size = self.game.relative_x(0.05)
        menu_font = pygame.font.SysFont("", menu_font_size)
        label_font_size = self.game.relative_x(0.04)
        label_font = pygame.font.SysFont("", label_font_size)

        return GameDiv(name="main_div", children=[
            GameTextElement(name="title",
                font=title_font, 
                text=CONFIG, 
                antialias=True, 
                color=(192, 192, 192),
                x=self.game.center_x(),
                y=self.game.relative_y(0.1),
            ),
            GameTextElement(name="back",
                font=menu_font, 
                text=BACK, 
                antialias=True, 
                color=(128, 128, 128),
                x=self.game.relative_x(0.10),
                y=self.game.relative_y(0.92),
                click=self.back_click,
                motion=self.motion,
            ),
            GameTextElement(name="quit",
                font=menu_font, 
                text=QUIT, 
                antialias=True, 
                color=(128, 128, 128),
                x=self.game.relative_x(0.91),
                y=self.game.relative_y(0.92),
                click=self.quit_click,
                motion=self.motion,
            ),
            ImageElement(name="ok",
                image=self.ok_image,
                x=self.game.relative_x(0.04),
                y=self.game.relative_y(0.26),
            ),
            GameDiv(name="options", x=self.game.relative_x(0.80), children=[
                GameDiv(x=self.game.relative_x(0.05), children=[
                    GameTextElement(name="minutes",
                        font=menu_font, 
                        text=str(self.data['minutes']), 
                        antialias=True, 
                        color=(192, 192, 128),
                        y=self.game.relative_y(0.30),
                    ),
                    GameTextElement(name="moves",
                        font=menu_font, 
                        text=str(self.data['moves']), 
                        antialias=True, 
                        color=(192, 192, 128),
                        y=self.game.relative_y(0.40),
                        condition=lambda: self.show_moves
                    ),
                    GameTextElement(name="bonus",
                        font=menu_font, 
                        text=str(self.data['bonus']), 
                        antialias=True, 
                        color=(192, 192, 128),
                        y=self.game.relative_y(0.40),
                        condition=lambda: self.show_bonus
                    ),
                ]),
                GameDiv(name="labels", children=[
                    GameTextElement(
                        font=label_font, 
                        text=MINUTES_LABEL, 
                        antialias=True, 
                        color=(96, 96, 96),
                        x=-self.game.relative_x(0.08),
                        y=self.game.relative_y(0.302),
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=MOVES_LABEL, 
                        antialias=True, 
                        color=(96, 96, 96),
                        x=-self.game.relative_x(0.08),
                        y=self.game.relative_y(0.402),
                        condition=lambda: self.show_moves
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=BONUS_LABEL, 
                        antialias=True, 
                        color=(96, 96, 96),
                        x=-self.game.relative_x(0.08),
                        y=self.game.relative_y(0.402),
                        condition=lambda: self.show_bonus
                    ),
                ]),
                GameDiv(name="plus", x=self.game.relative_x(0.1), children=[
                    GameTextElement(
                        font=label_font, 
                        text=PLUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.30),
                        motion=self.motion,
                        click=self.minutes_plus_click,
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=PLUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.40),
                        motion=self.motion,
                        click=self.moves_plus_click,
                        condition=lambda: self.show_moves
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=PLUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.40),
                        motion=self.motion,
                        click=self.bonus_plus_click,
                        condition=lambda: self.show_bonus
                    ),
                ]),
                GameDiv(name="minus", x=self.game.relative_x(0), children=[
                    GameTextElement(
                        font=label_font, 
                        text=MINUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.30),
                        motion=self.motion,
                        click=self.minutes_minus_click,
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=MINUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.40),
                        motion=self.motion,
                        click=self.moves_minus_click,
                        condition=lambda: self.show_moves
                    ),
                    GameTextElement(
                        font=label_font, 
                        text=MINUS, 
                        antialias=True, 
                        color=(96, 96, 96),
                        y=self.game.relative_y(0.40),
                        motion=self.motion,
                        click=self.bonus_minus_click,
                        condition=lambda: self.show_bonus
                    ),
                ]),
            ]),
            GameDiv(name="game_types", x=self.game.relative_x(0.30), children=[
                GameTextElement(name="minutes_per_game",
                    font=menu_font, 
                    text=MINUTES_PER_GAME, 
                    antialias=True, 
                    color=(128, 128, 128),
                    y=self.game.relative_y(0.30),
                    click=self.minutes_per_game_click,
                    motion=self.motion,
                ),
                GameTextElement(name="moves_per_minutes",
                    font=menu_font, 
                    text=MOVES_PER_MINUTES, 
                    antialias=True, 
                    color=(128, 128, 128),
                    y=self.game.relative_y(0.40),
                    click=self.moves_per_minutes_click,
                    motion=self.motion,
                ),
                GameTextElement(name="fischer_game",
                    font=menu_font, 
                    text=FISCHER_TIME, 
                    antialias=True, 
                    color=(128, 128, 128),
                    y=self.game.relative_y(0.50),
                    click=self.fischer_time_click,
                    motion=self.motion,
                ),
            ]),
        ])


    

