# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pieces.piece import Piece
from pieces.rook import Rook
from consts.colors import WHITE, next
from consts.moves import KINGSIDE_CASTLING, QUEENSIDE_CASTLING, NORMAL


class King(Piece):

    def name(self):
        return "king"

    def get_positions(self):
        return [
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 1),
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 1),
            (self.x, self.y - 1), (self.x, self.y + 1),
            (self.x - 1, self.y), (self.x + 1, self.y),
        ]

    def possible_moves(self):
        moves = self.get_positions()

        self.ignored = True
        hindered = self.board.hindered(next(self.color))
        self.ignored = False

        # Castling
        # Just valid for hindered = True
        # Neither King nor Rook hasn't moved
        # King's position shouldn't be hindered
        if (self.starting_position() and not self.position in hindered):
            kingside = self.board[(self.x + 3, self.y)]
            # King's new position shouldn't be hindered
            # Position between initial and final position shouldn't be hindered
            # and shouldn't have any pieces
            if (isinstance(kingside, Rook) and
                    not kingside.has_moved and
                    not (self.x + 1, self.y) in hindered and
                    not self.board[(self.x + 1, self.y)] and
                    not self.board[(self.x + 2, self.y)]):
                moves.append((self.x + 2, self.y, KINGSIDE_CASTLING))

            queenside = self.board[(self.x - 4, self.y)]
            # King's new position shouldn't be hindered
            # Position between initial and final position shouldn't be hindered
            # and shouldn't have any pieces between the king and the rook
            if (isinstance(queenside, Rook) and
                    not queenside.has_moved and
                    not (self.x - 1, self.y) in hindered and
                    not self.board[(self.x - 1, self.y)] and
                    not self.board[(self.x - 2, self.y)] and
                    not self.board[(self.x - 3, self.y)]):
                moves.append((self.x - 2, self.y, QUEENSIDE_CASTLING))

        move = {}
        enemy = {}
        self.ignored = True
        for position in moves:
            if not self.board.is_valid_position(position):
                continue
            if (position[0], position[1]) in hindered:
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
        self.ignored = False
        return move, enemy

    def attack_moves(self):
        return {
            position: NORMAL
            for position in self.get_positions()
            if self.valid_move(position)
        }

    def starting_position(self):
        """ True if king hasn't moved and is in the starting position """
        if self.has_moved:
            return False
        return self.position == ((4, 0) if self.color == WHITE else (4, 7))
