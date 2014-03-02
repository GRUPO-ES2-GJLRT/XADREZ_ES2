# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .test_board import TestBoard

from .test_rook import TestRook
from .test_knight import TestKnight
from .test_bishop import TestBishop
from .test_queen import TestQueen
from .test_king import TestKing



__all__ = [
    b'TestBoard',

    b'TestRook',
    b'TestKnight',
    b'TestBishop',
    b'TestQueen',
    b'TestKing',
]