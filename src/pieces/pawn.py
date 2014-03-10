# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from consts.colors import WHITE, BLACK
from consts.moves import EN_PASSANT, PROMOTION

from .piece import Piece

class Pawn(Piece):

    def name(self):
        return "pawn"

    def possible_moves(self, hindered=True):
        """ If hindered == False, it will return the attack moves """
        walk_moves = []
        attack_moves = []
        
        if self.color == WHITE:
            front = (self.x, self.y + 1)
            walk_moves.append(front)
            attack_moves.append((self.x - 1, self.y + 1))
            attack_moves.append((self.x + 1, self.y + 1))
            if self.y == 1 and not self.board[front]:
                walk_moves.append((self.x, self.y + 2))
        
        else:
            front = (self.x, self.y - 1)
            walk_moves.append(front)
            attack_moves.append((self.x - 1, self.y - 1))
            attack_moves.append((self.x + 1, self.y - 1))
            if self.y == 6 and not self.board[front]:
                walk_moves.append((self.x, self.y - 2))

        # En Passant
        if hindered and self.board.last_move:
            piece = self.board[self.board.last_move[2]]
            distance = abs(self.board.last_move[1][1] - self.board.last_move[2][1])
            if piece and piece.name() == "pawn" and distance == 2:
                if self.color == WHITE:
                    if piece.x == self.x - 1:
                        walk_moves.append((self.x - 1, self.y + 1, EN_PASSANT))
                    if piece.x == self.x + 1:
                        walk_moves.append((self.x + 1, self.y + 1, EN_PASSANT))   
                else:
                    if piece.x == self.x - 1:
                        walk_moves.append((self.x - 1, self.y - 1, EN_PASSANT))
                    if piece.x == self.x + 1:
                        walk_moves.append((self.x + 1, self.y - 1, EN_PASSANT)) 

        result = set(self.update_promotion(position) for position in attack_moves if self.valid_attack_move(position, hindered))
        if hindered:
            result = result.union(set(self.update_promotion(position) for position in walk_moves if self.valid_walk_move(position)))
        return result

    def update_promotion(self, position): 
        if (self.color == WHITE and position[1] == 7) or (self.color == BLACK and position[1] == 0):
            return (position[0], position[1], PROMOTION)
        return position

    def valid_walk_move(self, position):
        """ Checks if a position is not occupied by a piece 
        and is inside the board
        """
        if not self.board.valid(position):
            return False
        piece = self.board[position]
        if piece:
            return False
        return True

    def valid_attack_move(self, position, hindered):
        """ Checks if a position is occupied by an enemy piece 
        and is inside the board
        """
        if not hindered:
            return self.valid_move(position)
        if not self.board.valid(position):
            return False
        piece = self.board[position]
        if piece and piece.color != self.color:
            return True
        return False

