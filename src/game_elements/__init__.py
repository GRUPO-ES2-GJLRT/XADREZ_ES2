# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .player import Player
from .ai_player import AIPlayer
from .input_player import InputPlayer
from .online_player import OnlinePlayer


def create_player(color, timer, chess, level=None):
    if level is None:
        return InputPlayer(color, timer, chess)
    if level == -1:
    	return OnlinePlayer(color, timer, chess)
    return AIPlayer(color, timer, chess, level)

__all__ = [
    b'Player',
    b'AIPlayer',
    b'InputPlayer',
    b'OnlinePlayer',
    b'create_player',
]
