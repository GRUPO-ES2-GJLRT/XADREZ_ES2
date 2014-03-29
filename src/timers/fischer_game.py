# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from datetime import timedelta

from .minutes_per_game import MinutesPerGameTimer
from .base import PlayerTimer


class FischerGameTimer(MinutesPerGameTimer):

    def __init__(self, data):
        super(FischerGameTimer, self).__init__(data)
        self.bonus = timedelta(seconds=data["bonus"])

    def stop_turn(self):
        PlayerTimer.stop_turn(self)
        self.time += self.bonus
