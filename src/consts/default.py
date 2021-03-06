# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

TIMER_OPTIONS = {
    "minutes_per_game": 1,
    "moves_per_minutes": 2,
    "fischer_game": 3,
}

FIFTY_MOVE_OPTIONS = {
    "auto": 1,
    "button": 2,
    "disable": 3,
}

JIT_DRAW_OPTIONS = {
    "disable": 0,
    "enable": 1,
}

TIMEOUT_OPTIONS = {
    "1s": 1,
    "2s": 2,
    "3s": 3,
    "5s": 5,
    "8s": 8,
    "13s": 13,
    "21s": 21,
    "34s": 34,
}

TIMER = TIMER_OPTIONS["minutes_per_game"]
MINUTES = 10
MOVES = 10
BONUS = 10
TIMEOUT = 13
FIFTY_MOVE = FIFTY_MOVE_OPTIONS["auto"]
JIT_DRAW = JIT_DRAW_OPTIONS["enable"]

from timers.minutes_per_game import MinutesPerGameTimer
from timers.moves_per_minute import MovesPerMinuteTimer
from timers.fischer_game import FischerGameTimer

TIMER_CLASS = {
    1: MinutesPerGameTimer,
    2: MovesPerMinuteTimer,
    3: FischerGameTimer,
}
