from pygame import font
from .interface import Interface
from .elements import (
    GameDiv, 
    ImageElement, 
    RectElement,
    GameTextElement, 
    PiecesElement, 
    SquareElement,
)

from consts.colors import BLACK, WHITE
from consts.i18n import *

MARGIN = 28
BORDER = 2
RIGHT_MARGIN = 14

class ChessInterface(Interface):

    def interface(self):
        _font = font.SysFont("", 26)
        time_font = font.SysFont("", 48)
        message_font = font.SysFont("", 148)
        return GameDiv(name="main_div", children=[
            RectElement(x=MARGIN, color=(0, 0, 0),
                size_x=self.board_size + 2 * BORDER,
                size_y=self.board_size + 2 * BORDER,
                children=[
                    GameDiv(x=BORDER, y=BORDER, children=[
                        ImageElement(self.board_image),
                        SquareElement(
                            color=(0, 223, 0),
                            square_size=self.square_size, 
                            square=lambda: self.selected
                        ),
                        SquareElement(
                            color=(255, 150, 150),
                            square_size=self.square_size, 
                            square=lambda: self.fail
                        ),
                        SquareElement(
                            color=(204, 153, 255),
                            square_size=self.square_size, 
                            square=lambda: self.check
                        ),
                        PiecesElement(
                            board=self.board,
                            square_size=self.square_size,
                            piece_images=self.piece_images,
                        ),
                    ]),
                ],
            ),
            GameDiv(x=13, y=BORDER + self.square_size // 2, children=[
                GameTextElement(y=(7 - i) * self.square_size,
                    font=_font, 
                    text=str(label_text), 
                    antialias=True, 
                    color=(128, 128, 128), 
                ) for i, label_text in enumerate(['1', '2', '3', '4', '5', '6', '7', '8'])
            ]),
            GameDiv(x=MARGIN + BORDER + self.square_size // 2, 
                y=17 + self.board_size + BORDER, children=[
                GameTextElement(x=i * self.square_size,
                    font=_font, 
                    text=str(label_text), 
                    antialias=True, 
                    color=(128, 128, 128), 
                ) for i, label_text in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
            ]),
            GameDiv(name="info_div", children=[
                GameDiv(name="white_div", children=[
                    GameTextElement(name="white_time", y=self.square_size // 2,
                        font=time_font, 
                        text=str("20:00"), 
                        antialias=True, 
                        color=(128, 128, 128),
                    ),
                    ImageElement(self.piece_images['%s_king' % WHITE]),
                    ImageElement(name="white_arrow",
                        image=None, 
                        condition=lambda: self.board.current_color == WHITE
                    ),
                ]),
                GameDiv(name="black_div", children=[
                    GameTextElement(name="black_time", y=self.square_size // 2,
                        font=time_font, 
                        text=str("20:00"), 
                        antialias=True, 
                        color=(128, 128, 128),
                    ),
                    ImageElement(self.piece_images['%s_king' % BLACK]),
                    ImageElement(name="black_arrow",
                        image=None, 
                        condition=lambda: self.board.current_color == BLACK
                    ),
                ]),
            ]),
            GameDiv(x=self.board_size // 2 + MARGIN + BORDER, 
                y=self.board_size // 2 + BORDER, children=[
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
                    condition=lambda: self.draw_state
                ),
                GameTextElement(
                    font=message_font, 
                    text=BLACK_WINS_MESSAGE, 
                    antialias=True, 
                    color=(50, 50, 50), 
                    style="outline", 
                    other_color=(255, 255, 255),
                    condition=lambda: self.black_wins
                ),
                GameTextElement(
                    font=message_font, 
                    text=WHITE_WINS_MESSAGE, 
                    antialias=True, 
                    color=(255, 255, 255), 
                    style="outline", 
                    other_color=(50, 50, 50),
                    condition=lambda: self.white_wins
                ),
            ]),
        ])

    def resize(self):
        if self.horizontal:
            self.info_div.x = self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN)
            self.info_div.y = 0

            self.white_div.x = 0
            self.white_div.y = self.game.height - (MARGIN + 2*BORDER) - self.square_size
            self.white_time.x = self.square_size + MARGIN + RIGHT_MARGIN
            self.white_arrow.image = self.arrow_down
            self.white_arrow.x = self.square_size // 4
            self.white_arrow.y = -self.square_size // 2

            self.black_div.x = 0
            self.black_div.y = BORDER
            self.black_time.x = self.square_size + MARGIN + RIGHT_MARGIN
            self.black_time.y = self.square_size // 2
            self.black_arrow.image = self.arrow_up
            self.black_arrow.x = self.square_size // 4
            self.black_arrow.y = self.square_size
        else:
            self.info_div.x = 0
            self.info_div.y = self.board_size + 2*BORDER + MARGIN

            self.white_div.x = self.board_size + (MARGIN + 2*BORDER) - self.square_size
            self.white_div.y = 0
            self.white_time.x = - MARGIN - RIGHT_MARGIN - self.square_size // 2
            self.white_arrow.image = self.arrow_right
            self.white_arrow.x = -self.square_size // 2
            self.white_arrow.y = self.square_size // 4
            
            self.black_div.x = MARGIN + 2*BORDER
            self.black_div.y = 0
            self.black_time.x = self.square_size + MARGIN + RIGHT_MARGIN + self.square_size // 2
            self.black_arrow.image = self.arrow_left
            self.black_arrow.x = self.square_size
            self.black_arrow.y = self.square_size // 4

