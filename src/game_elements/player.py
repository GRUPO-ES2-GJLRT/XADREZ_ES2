# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from consts.colors import next

SELECT = 0
PLAY = 1
END = 2


class Player(object):

    def __init__(self, color, timer, chess):
        self.color = color
        self.timer = timer
        self.chess = chess
        self.state = None
        self.timer.player = self
        self.timer.start()

    def start_turn(self):
        self.timer.start_turn()
        self.state = SELECT

    def end_turn(self):
        self.timer.end_turn()
        self.state = None

    def pause_turn(self):
        self.timer.end_turn()

    def resume_turn(self):
        self.timer.start_turn()

    def lose(self):
        self.chess.win(next(self.color))

    def select(self, square):
        self.chess.select(square)
        self.state = PLAY

    def play(self, square):
        moved = self.chess.play(square)
        self.state = PLAY if not moved else self.state
        return moved

    def click(self, square):
        pass
