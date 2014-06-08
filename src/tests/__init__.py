# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from .test_board import TestBoard
from .test_rook import TestRook
from .test_knight import TestKnight
from .test_bishop import TestBishop
from .test_queen import TestQueen
from .test_king import TestKing
from .test_pawn import TestPawn
from .test_cython_functions import TestCythonFunctions
from .test_ai import TestAI
from .test_player import TestPlayer
from .test_online_chess import TestOnlineChess


__all__ = [
    b'TestBoard',
    b'TestRook',
    b'TestKnight',
    b'TestBishop',
    b'TestQueen',
    b'TestKing',
    b'TestPawn',
    b'TestCythonFunctions',
    b'TestAI',
    b'TestPlayer',
    b'TestOnlineChess',
]
