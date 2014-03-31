# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os import path
from functools import partial

from pygame import (
    font,
    image,
    transform,
)

from .interface import Interface

from scenes.elements import (
    GameDiv,
    GameTextElement,
    ImageElement,
    PiecesElement,
    RectElement,
    SquareElement
)

from consts.colors import BLACK, WHITE
from consts.i18n import (
    CHECK_MESSAGE, DRAW_MESSAGE, BLACK_WINS_MESSAGE, WHITE_WINS_MESSAGE
)

GAME_DRAW = 0
WHITE_WINS = 1
BLACK_WINS = 2

MARGIN = 28
BORDER = 2
RIGHT_MARGIN = 14

B2 = 2 * BORDER
MRM = MARGIN + RIGHT_MARGIN


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in xrange(ord(c1), ord(c2) + 1):
        yield chr(c)


class ChessInterface(Interface):

    def interface(self):
        self.calculate_size()
        self.load_images()

        _font = lambda: font.SysFont("", int(0.03 * self.board_size))
        time_font = lambda: font.SysFont("", int(0.06 * self.board_size))
        message_font = lambda: font.SysFont("", int(0.2 * self.board_size))
        return GameDiv(name="main_div", children=[
            RectElement(
                x=MARGIN,
                color=(0, 0, 0),
                size_x=lambda: self.board_size + B2,
                size_y=lambda: self.board_size + B2,
                children=[
                    GameDiv(
                        x=BORDER,
                        y=BORDER,
                        children=[
                            ImageElement(
                                image=lambda: self.board_image
                            ),
                            SquareElement(
                                color=(0, 223, 0),
                                square_size=lambda: self.square_size,
                                square=lambda: self.selected
                            ),
                            SquareElement(
                                color=(255, 150, 150),
                                square_size=lambda: self.square_size,
                                square=lambda: self.fail
                            ),
                            SquareElement(
                                color=(204, 153, 255),
                                square_size=lambda: self.square_size,
                                square=lambda: self.check
                            ),
                            PiecesElement(
                                board=self.board,
                                square_size=lambda: self.square_size,
                                piece_images=lambda: self.piece_images,
                            ),
                        ]
                    ),
                ],
            ),
            GameDiv(
                x=13,
                y=lambda: BORDER + self.square_size // 2,
                children=[
                    GameTextElement(
                        y=partial((lambda x: (7 - x) * self.square_size), x=i),
                        font=_font,
                        text=str(label_text),
                        antialias=True,
                        color=(128, 128, 128),
                    ) for i, label_text in enumerate(range(1, 9))
                ]
            ),
            GameDiv(
                x=lambda: MARGIN + BORDER + self.square_size // 2,
                y=lambda: 17 + self.board_size + BORDER,
                children=[
                    GameTextElement(
                        x=partial((lambda x: x * self.square_size), x=i),
                        font=_font,
                        text=str(label_text),
                        antialias=True,
                        color=(128, 128, 128),
                    ) for i, label_text in enumerate(char_range('A', 'H'))
                ]
            ),
            GameDiv(
                name="info_div",
                x=lambda: (self.board_size + (B2 + MRM)
                           if self.horizontal
                           else 0),
                y=lambda: (0
                           if self.horizontal
                           else self.board_size + B2 + MARGIN),
                children=[
                    GameDiv(
                        name="white_div",
                        x=lambda: (0
                                   if self.horizontal
                                   else (self.board_size + (MARGIN + B2) -
                                         self.square_size)),
                        y=lambda: ((self.game.height - (MARGIN + B2) -
                                   self.square_size)
                                   if self.horizontal
                                   else 0),
                        children=[
                            GameTextElement(
                                name="white_time",
                                x=lambda: ((self.square_size + MRM)
                                           if self.horizontal
                                           else - MRM - self.square_size // 2),
                                y=lambda: self.square_size // 2,
                                text=lambda: self.white_minutes(),
                                redraw=True,
                                font=time_font,
                                antialias=True,
                                color=(128, 128, 128),
                            ),
                            ImageElement(
                                image=lambda: self.piece_images['%s_king' %
                                                                WHITE]
                            ),
                            ImageElement(
                                name="white_arrow",
                                image=lambda: (self.arrow_down
                                               if self.horizontal
                                               else self.arrow_right),
                                x=lambda: (self.square_size // 4
                                           if self.horizontal
                                           else -self.square_size // 2),
                                y=lambda: (-self.square_size // 2
                                           if self.horizontal
                                           else self.square_size // 4),
                                condition=(
                                    lambda: self.board.current_color == WHITE)
                            ),
                        ]
                    ),
                    GameDiv(
                        name="black_div",
                        x=lambda: (0
                                   if self.horizontal
                                   else MARGIN + B2),
                        y=lambda: (BORDER
                                   if self.horizontal
                                   else 0),
                        children=[
                            GameTextElement(
                                name="black_time",
                                x=lambda: ((self.square_size + MRM)
                                           if self.horizontal
                                           else (self.square_size + MRM +
                                                 self.square_size // 2)),
                                y=lambda: self.square_size // 2,
                                text=lambda: self.black_minutes(),
                                redraw=True,
                                font=time_font,
                                antialias=True,
                                color=(128, 128, 128),
                            ),
                            ImageElement(
                                image=lambda: self.piece_images['%s_king' %
                                                                BLACK]
                            ),
                            ImageElement(
                                name="black_arrow",
                                image=lambda: (self.arrow_up
                                               if self.horizontal
                                               else self.arrow_left),
                                x=lambda: (self.square_size // 4
                                           if self.horizontal
                                           else self.square_size),
                                y=lambda: (self.square_size
                                           if self.horizontal
                                           else self.square_size // 4),
                                condition=(
                                    lambda: self.board.current_color == BLACK)
                            ),
                        ]
                    ),
                ]
            ),
            GameDiv(
                x=lambda: self.board_size // 2 + MARGIN + BORDER,
                y=lambda: self.board_size // 2 + BORDER,
                children=[
                    GameTextElement(
                        font=message_font,
                        text=CHECK_MESSAGE,
                        antialias=True,
                        color=(30, 144, 255),
                        style="outline",
                        other_color=(255, 255, 255),
                        condition=lambda: self.countdown
                    ),
                    GameTextElement(
                        font=message_font,
                        text=DRAW_MESSAGE,
                        antialias=True,
                        color=(30, 144, 255),
                        style="outline",
                        other_color=(255, 255, 255),
                        condition=lambda: self.state == GAME_DRAW
                    ),
                    GameTextElement(
                        font=message_font,
                        text=BLACK_WINS_MESSAGE,
                        antialias=True,
                        color=(50, 50, 50),
                        style="outline",
                        other_color=(255, 255, 255),
                        condition=lambda: self.state == BLACK_WINS
                    ),
                    GameTextElement(
                        font=message_font,
                        text=WHITE_WINS_MESSAGE,
                        antialias=True,
                        color=(255, 255, 255),
                        style="outline",
                        other_color=(50, 50, 50),
                        condition=lambda: self.state == WHITE_WINS
                    ),
                ]
            ),
        ])

    def calculate_size(self):
        """ Calculates the board size, square size and the orientation. """
        max_board_size = min(
            self.game.width - (MARGIN + 2 * BORDER),
            self.game.height - (MARGIN + 2 * BORDER)
        )

        self.horizontal = True
        self.square_size = (max_board_size // 8)
        self.board_size = self.square_size * 8
        if self.game.width - self.board_size < 3 * self.square_size:
            max_board_size = min(
                self.game.width - (MARGIN + 2 * BORDER),
                self.game.height - (MARGIN + 2 * BORDER) - 100
            )

            self.horizontal = False
            self.square_size = (max_board_size // 8)
            self.board_size = self.square_size * 8

    def load_images(self):
        self.board_image_original = image.load(
            path.join(self.assets_dir, 'chess_board.png'))

        self.piece_images_original = {}
        for color in [BLACK, WHITE]:
            for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                img = image.load(path.join(
                    self.assets_dir,
                    "%s_%s.png" % (color, piece))
                )
                self.piece_images_original["%s_%s" % (color, piece)] = img

        self.arrow_down_original = image.load(
            path.join(self.assets_dir, 'arrow_down.png')
        )
        self.transform_images()

    def transform_images(self):
        self.board_image = transform.scale(
            self.board_image_original,
            (self.board_size, self.board_size)
        )
        self.piece_images = {}
        for key, piece_image in self.piece_images_original.items():
            self.piece_images[key] = transform.scale(
                piece_image,
                (self.square_size, self.square_size)
            )
        self.arrow_down = transform.scale(
            self.arrow_down_original,
            (self.square_size // 2, self.square_size // 2)
        )
        self.arrow_up = transform.rotate(self.arrow_down, 180)
        self.arrow_left = transform.rotate(self.arrow_down, 270)
        self.arrow_right = transform.rotate(self.arrow_down, 90)

    def resize(self):
        self.calculate_size()
        self.transform_images()
        self.main_div.call('redraw')
