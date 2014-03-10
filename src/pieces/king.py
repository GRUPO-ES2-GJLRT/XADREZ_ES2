# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from .piece import Piece
from consts.colors import BLACK, WHITE, next
from consts.moves import CASTLING

class King(Piece):

    def name(self):
        return "king"

    def possible_moves(self, hindered=True):
        moves = [
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 1), 
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 1),
            (self.x, self.y - 1), (self.x, self.y + 1),
            (self.x - 1, self.y), (self.x + 1, self.y),
        ]

        hindered_positions = self.board.hindered(next(self.color)) if hindered else set()
        
        # Castling
        # Just valid for hindered = True
        # Neither King nor Rook hasn't moved
        # King's position shouldn't be hindered
        if hindered and self.starting_position() and not self.is_hindered(hindered=hindered_positions):
            kingside = self.board[(self.x + 3, self.y)]
            # King's new position shouldn't be hindered
            # Position between King initial and final position shouldn't be hindered 
            # and shouldn't have any pieces
            if (kingside and kingside.name() == "rook" and 
                not kingside.has_moved and 
                not self.is_hindered(position=(self.x + 1, self.y), hindered=hindered_positions) and
                not self.board[(self.x + 1, self.y)] and 
                not self.board[(self.x + 2, self.y)]):
                moves.append((self.x + 2, self.y, CASTLING))

            queenside = self.board[(self.x - 4, self.y)]
            # King's new position shouldn't be hindered
            # Position between King initial and final position shouldn't be hindered 
            # and shouldn't have any pieces between the king and the rook
            if (queenside and queenside.name() == "rook" and 
                not queenside.has_moved and 
                not self.is_hindered(position=(self.x - 1, self.y), hindered=hindered_positions) and
                not self.board[(self.x - 1, self.y)] and 
                not self.board[(self.x - 2, self.y)] and 
                not self.board[(self.x - 3, self.y)]):
                moves.append((self.x - 2, self.y, CASTLING))

        return set(
            position for position in moves if self.valid_move(position) and
            not self.is_hindered(position=position, hindered=hindered_positions)
        )

    def starting_position(self):
        """ Return True if king hasn't moved and is in the starting position """
        if self.has_moved:
            return False
        return self.position() == ((4, 0) if self.color == WHITE else (4, 7))

