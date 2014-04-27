# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from threading import Thread

from .piece import Piece


class ThreadedPiece(Thread, Piece):

    def __init__(self, board, color, x, y):
        super(ThreadedPiece, self).__init__()
        super(ThreadedPiece, self).__init__(board, color, x, y)