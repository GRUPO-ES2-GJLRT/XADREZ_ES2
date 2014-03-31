# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


import threading

from datetime import datetime


class PlayerTimer(threading.Thread):

    def __init__(self):
        super(PlayerTimer, self).__init__()
        self.event = threading.Event()
        self.stopped = True
        self.last_time = datetime.now()
        self.player = None
        self.lost = False

    def run(self):
        while not self.event.wait(0.5):
            if not self.stopped:
                new_time = datetime.now()
                delta = (new_time - self.last_time)
                self.update_time(delta)
                self.last_time = new_time

    def lose(self):
        self.lost = True
        if self.player:
            self.player.lose()

    def start_turn(self):
        self.stopped = False
        self.last_time = datetime.now()

    def end_turn(self):
        self.stopped = True

    def update_time(self, delta):
        pass

    def minutes_to_text(self):
        pass
