# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from copy import deepcopy
from consts.moves import NORMAL
from consts.colors import WHITE


class BoardInterface(object):
    """ 'Public' interface for board """

    def __init__(self, new_game=True):
        self.current_color = WHITE

    def clone(self):
        """ Clone this board """
        return deepcopy(self)

    def hindered(self, color):
        """ Return a set of positions attacked by color """
        return set()

    def possible_moves(self, color):
        """ Return a set of possible moves """
        return set()

    def possible_killing_moves(self, color):
        """ Return a set of valid attack moves """
        return set()

    def current_king_position(self):
        """ Return the position of the king that is playing """
        return (-1, -1)

    def move(self, original_position, new_position, skip_validation=False):
        """ Move a piece. Return true, if piece has moved """
        return False

    def status(self, possible_moves=None):
        """ Return the status of the board:
            CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE, NORMAL
        """
        return NORMAL

    def at(self, position):
        """ Return the piece "color name" at position """
        return None

    def load_fen(self, fen):
        """ Parse a fen string to setup the board """
        pass

    def get_pieces(self):
        """ Return an iterable of pieces.
            Required piece attributes: name, position, color
        """
        return []

    @staticmethod
    def is_valid_position(position):
        """ Check if position is inside the board """
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    @staticmethod
    def chess_notation_to_position(chess_notation):
        """ Convert chess notation (a1) to position (0, 0) """
        return (
            ord(chess_notation[0]) - 97,
            int(chess_notation[1]) - 1
        )
