# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

TIMER_OPTIONS = {
    "minutes_per_game": 1,
    "moves_per_minutes": 2,
    "fischer_game": 3,
}

TIMER = TIMER_OPTIONS["minutes_per_game"]
MINUTES = 10
MOVES = 10
BONUS = 10

from timers.minutes_per_game import MinutesPerGameTimer
from timers.moves_per_minute import MovesPerMinuteTimer
from timers.fischer_game import FischerGameTimer

TIMER_CLASS = {
    1: MinutesPerGameTimer,
    2: MovesPerMinuteTimer,
    3: FischerGameTimer,
}
