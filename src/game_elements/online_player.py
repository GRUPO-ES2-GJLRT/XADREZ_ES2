# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import random
import sys
from os import path
import threading
from collections import Counter
from time import sleep
from consts.moves import (
    CHECKMATE, STALEMATE
)
from consts.end_game import END_GAME, PAUSE
from consts.pieces import PAWN, KING
from consts.colors import WHITE, BLACK
from .player import Player, END
from cython.constants import ILLEGAL, LEGAL, EMPTY
from cython.board import move_key
from cython.functions import *

class OnlinePlayer(Player):

    def __init__(self, color, timer, chess, *args, **kwargs):
        super(OnlinePlayer, self).__init__(color, timer, chess, *args, **kwargs)
        
    def start_turn(self):
        if not self.chess.game.running:
            sys.exit()
        super(OnlinePlayer, self).start_turn()
        threading.Thread(target=self.online_move).start()

    def select(self, square):
        super(OnlinePlayer, self).select(square)
        sleep(0.1)

    def online_move(self):
        if (self.state == END or self.chess.state in END_GAME):
            return
        
        while self.chess.running:
            self.try_to_exit_thread_loop()
            tup = self.chess.wait_move_validation();
            if not tup:
                return
            self.select(tup[0])
            if self.play(tup[1], tup[2]):
                self.chess.do_jit_draw()
                return

    def confirm_draw(self):
        self.chess.request_draw()
