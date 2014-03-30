# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

SELECT = 0
PLAY = 1
END = 2


class Player(object):

    def __init__(self, color, timer):
        self.color = color
        self.timer = timer
        self.state = None
        self.timer.start()

    def start_turn(self):
        self.timer.start_turn()
        self.state = SELECT

    def end_turn(self):
        self.timer.end_turn()
        self.state = None