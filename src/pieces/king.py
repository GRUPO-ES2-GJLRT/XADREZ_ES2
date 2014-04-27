# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pieces.piece import Piece
from consts.colors import WHITE, next
from consts.moves import KINGSIDE_CASTLING, QUEENSIDE_CASTLING, NORMAL


class King(Piece):

    def name(self):
        return "king"

    def possible_moves(self, hindered=True, hindered_positions=None):
        moves = [
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 1),
            (self.x, self.y - 1), (self.x, self.y + 1),
            (self.x - 1, self.y), (self.x + 1, self.y),
        ]

        if not hindered_positions:
            hindered_positions = (self.board.hindered(next(self.color))
                                  if hindered else set())

        # Castling
        # Just valid for hindered = True
        # Neither King nor Rook hasn't moved
        # King's position shouldn't be hindered
        if (hindered and self.starting_position() and not
                self.is_hindered(hindered=hindered_positions)):
            kingside = self.board[(self.x + 3, self.y)]
            # King's new position shouldn't be hindered
            # Position between initial and final position shouldn't be hindered
            # and shouldn't have any pieces
            if (kingside and kingside.name() == "rook" and
                    not kingside.has_moved and
                    not self.is_hindered(position=(self.x + 1, self.y),
                                         hindered=hindered_positions) and
                    not self.board[(self.x + 1, self.y)] and
                    not self.board[(self.x + 2, self.y)]):
                moves.append((self.x + 2, self.y, KINGSIDE_CASTLING))

            queenside = self.board[(self.x - 4, self.y)]
            # King's new position shouldn't be hindered
            # Position between initial and final position shouldn't be hindered
            # and shouldn't have any pieces between the king and the rook
            if (queenside and queenside.name() == "rook" and
                    not queenside.has_moved and
                    not self.is_hindered(position=(self.x - 1, self.y),
                                         hindered=hindered_positions) and
                    not self.board[(self.x - 1, self.y)] and
                    not self.board[(self.x - 2, self.y)] and
                    not self.board[(self.x - 3, self.y)]):
                moves.append((self.x - 2, self.y, QUEENSIDE_CASTLING))

        move = {}
        enemy = {}
        for position in moves:
            if not self.board.is_valid_position(position):
                continue
            if self.is_hindered(position=position,
                                hindered=hindered_positions):
                continue
            piece = self.board[position]
            temp = move
            if piece and not piece.ignored:
                if piece.color == self.color:
                    continue
                else:
                    temp = enemy

            temp[(position[0], position[1])] = (
                position[2] if len(position) == 3 else NORMAL)
        return move, enemy

    def starting_position(self):
        """ True if king hasn't moved and is in the starting position """
        if self.has_moved:
            return False
        return self.position == ((4, 0) if self.color == WHITE else (4, 7))
