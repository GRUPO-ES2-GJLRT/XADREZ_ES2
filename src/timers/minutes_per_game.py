# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from datetime import timedelta

from .base import PlayerTimer


class MinutesPerGameTimer(PlayerTimer):

    def __init__(self, data):
        super(MinutesPerGameTimer, self).__init__()
        self.time = timedelta(minutes=data["minutes"])
        self.zero = timedelta()

    def update_time(self, delta):
        self.time -= delta
        if self.time < self.zero:
            self.time = self.zero
            self.lose()
            self.event.set()

    def minutes_to_text(self):
        hours, remainder = divmod(self.time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "%02d:%02d" % (minutes, seconds)
