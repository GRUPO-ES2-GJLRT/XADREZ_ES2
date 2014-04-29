# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .player import Player, PLAY
from consts.colors import WHITE, BLACK


class InputPlayer(Player):

    def __init__(self, color, timer, chess, *args, **kwargs):
        super(InputPlayer, self).__init__(color, timer, chess, *args, **kwargs)

    def click(self, square):
        if square:
            piece = self.chess.board.at(square)
            if piece and {'w': WHITE, 'b': BLACK}[piece[0]] == self.color:
                self.select(square)
            elif self.state == PLAY:
                self.play(square)

    def confirm_draw(self):
        self.chess.confirm_draw_dialog(self)
