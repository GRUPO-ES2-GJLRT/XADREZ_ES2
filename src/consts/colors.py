# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

WHITE = 0
BLACK = 1

next = lambda color: BLACK if color == WHITE else WHITE
