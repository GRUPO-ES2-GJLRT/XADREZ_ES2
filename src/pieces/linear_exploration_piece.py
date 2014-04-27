# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .piece import Piece
from consts.moves import NORMAL


class LinearExplorationPiece(Piece):

    def explore_position(self, position, move, enemy, ally, allowed):
        if not self.board.is_valid_position(position):
            return False

        if not position in allowed:
            move, enemy, ally = {}, {}, {}

        piece = self.board[position]
        if piece and not piece.ignored:
            if piece.color == self.color:
                ally[position] = NORMAL
            else:
                enemy[position] = NORMAL
            return False

        move[position] = NORMAL
        return True
