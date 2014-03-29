# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import Piece
from consts.moves import NORMAL


class LinearExplorationPiece(Piece):

    def explore_position_and_continue(self, position, result):
        if self.valid_move(position):
            result[position] = NORMAL

        # stop if invalid position
        if not self.board.valid(position):
            return False

        # continue if there is no piece
        piece = self.board[position]
        return not piece or (piece and piece.ignored)
