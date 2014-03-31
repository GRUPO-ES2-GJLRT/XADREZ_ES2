# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

QUEENSIDE_CASTLING = 'queenside castling'
KINGSIDE_CASTLING = 'kingside castling'

LEFT_EN_PASSANT = 'left en passant'
RIGHT_EN_PASSANT = 'right en passant'

PROMOTION = 'promotion'
NORMAL = 'normal'

to_move_dict = lambda lis: {
    (position[0], position[1]): (position[2] if len(position) == 3 else NORMAL)
    for position in lis
}

CHECK = "check"
CHECKMATE = "checkmate"
STALEMATE = "stalemate"
FIFTY_MOVE = "fifty move"
