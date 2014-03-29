# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from datetime import timedelta

from .minutes_per_game import MinutesPerGameTimer
from .base import PlayerTimer


class MovesPerMinuteTimer(MinutesPerGameTimer):

    def __init__(self, data):
        super(MovesPerMinuteTimer, self).__init__(data)
        self.expected_moves = data["moves"]
        self.count_up = timedelta(0)
        self.current_moves = 0

    def update_time(self, delta):
        MinutesPerGameTimer.update_time(self, delta)
        self.count_up += delta
        if self.count_up.seconds >= 60.0:
            if self.current_moves < self.expected_moves:
                self.lose = True
                self.event.set()
            else:
                self.count_up = timedelta(0)
                self.current_moves = 0

    def stop_turn(self):
        PlayerTimer.stop_turn(self)
        self.current_moves += 1
