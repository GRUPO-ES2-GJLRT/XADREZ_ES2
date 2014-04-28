# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from consts.colors import WHITE, BLACK
from consts.moves import (
    LEFT_EN_PASSANT, RIGHT_EN_PASSANT, PROMOTION, NORMAL,
)

from .piece import Piece


class Pawn(Piece):

    def name(self):
        return "pawn"

    def possible_moves(self):
        moves = {}
        enemy = {}

        _, allowed = self.get_allowed()
        if self.color == WHITE:
            front = (self.x, self.y + 1)
            self.add_walk_move(front, moves, allowed)
            self.add_attack_move((self.x - 1, self.y + 1), enemy, allowed)
            self.add_attack_move((self.x + 1, self.y + 1), enemy, allowed)
            if self.y == 1 and not self.board[front]:
                self.add_walk_move((self.x, self.y + 2), moves, allowed)

        else:
            front = (self.x, self.y - 1)
            self.add_walk_move(front, moves, allowed)
            self.add_attack_move((self.x - 1, self.y - 1), enemy, allowed)
            self.add_attack_move((self.x + 1, self.y - 1), enemy, allowed)
            if self.y == 6 and not self.board[front]:
                self.add_walk_move((self.x, self.y - 2), moves, allowed)

        # En Passant
        if self.board.last_move:
            passant = None
            piece = self.board[self.board.last_move[2]]
            distance = abs(self.board.last_move[1][1] -
                           self.board.last_move[2][1])
            if isinstance(piece, Pawn) and distance == 2 and piece.y == self.y:
                if self.color == WHITE:
                    if piece.x == self.x - 1:
                        passant = (self.x - 1, self.y + 1, LEFT_EN_PASSANT)
                    if piece.x == self.x + 1:
                        passant = (self.x + 1, self.y + 1, RIGHT_EN_PASSANT)
                else:
                    if piece.x == self.x - 1:
                        passant = (self.x - 1, self.y - 1, LEFT_EN_PASSANT)
                    if piece.x == self.x + 1:
                        passant = (self.x + 1, self.y - 1, RIGHT_EN_PASSANT)
            if passant:
                modifier = passant[2]
                position = (passant[0], passant[1])
                if (self.valid_walk_move(position) and position in allowed):
                    enemy[position] = modifier

        return moves, enemy

    def add_walk_move(self, position, moves, allowed):
        if (self.valid_walk_move(position) and position in allowed):
            moves[position] = self.modifier(position)

    def add_attack_move(self, position, attack, allowed):
        if (self.valid_attack_move(position) and position in allowed):
            attack[position] = self.modifier(position)

    def attack_moves(self):
        if self.color == WHITE:
            positions = [(self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
        else:
            positions = [(self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]

        return {
            position: self.modifier(position)
            for position in positions
            if self.valid_move(position)
        }

    def modifier(self, position):
        if ((self.color == WHITE and position[1] == 7) or
                (self.color == BLACK and position[1] == 0)):
            return PROMOTION
        return NORMAL

    def valid_walk_move(self, position):
        """ Checks if a position is not occupied by a piece
        and is inside the board
        """
        if not self.board.is_valid_position(position):
            return False
        piece = self.board[position]
        if piece:
            return False
        return True

    def valid_attack_move(self, position):
        """ Checks if a position is occupied by an enemy piece
        and is inside the board
        """
        if not self.board.is_valid_position(position):
            return False
        piece = self.board[position]
        if piece and piece.color != self.color:
            return True
        return False
