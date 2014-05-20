# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from consts.colors import WHITE, BLACK

CHECK_COUNTDOWN = 0.5


GAME_DRAW = 0
WHITE_WINS = 1
BLACK_WINS = 2
PAUSE = 3
MAX_DRAW_DELTA = 0.5


END_GAME = [GAME_DRAW, WHITE_WINS, BLACK_WINS]

WINS = {
    WHITE: WHITE_WINS,
    BLACK: BLACK_WINS,
}