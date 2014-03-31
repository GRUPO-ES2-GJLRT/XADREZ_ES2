# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from.game_div import GameDiv


class ChessElement(GameDiv):

    def position_rect(self, position, x=0, y=0):
        return (
            x + position[0] * self.square_size,
            y + (7 - position[1]) * self.square_size,
            self.square_size,
            self.square_size
        )
