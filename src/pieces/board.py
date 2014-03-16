# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from consts.colors import WHITE, BLACK, next
from consts.moves import LEFT_EN_PASSANT, RIGHT_EN_PASSANT, PROMOTION, NORMAL, QUEENSIDE_CASTLING, KINGSIDE_CASTLING, \
    CHECK

from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King


class Board(object):
    def __init__(self, new_game=True):
        self.board_data = [
            [None for x in xrange(8)] for y in xrange(8)
        ]
        self.pieces = {
            WHITE: [],
            BLACK: [],
        }
        self.kings = {
            WHITE: None,
            BLACK: None,
        }
        if new_game:
            # Pawn
            for x in xrange(8):
                Pawn(self, WHITE, x, 1)
                Pawn(self, BLACK, x, 6)
            # Rook
            Rook(self, WHITE, 0, 0)
            Rook(self, WHITE, 7, 0)
            Rook(self, BLACK, 0, 7)
            Rook(self, BLACK, 7, 7)
            # Knight
            Knight(self, WHITE, 1, 0)
            Knight(self, WHITE, 6, 0)
            Knight(self, BLACK, 1, 7)
            Knight(self, BLACK, 6, 7)
            # Bishop
            Bishop(self, WHITE, 2, 0)
            Bishop(self, WHITE, 5, 0)
            Bishop(self, BLACK, 2, 7)
            Bishop(self, BLACK, 5, 7)
            # Queen
            Queen(self, WHITE, 3, 0)
            Queen(self, BLACK, 3, 7)
            # King
            King(self, WHITE, 4, 0)
            King(self, BLACK, 4, 7)
        self.last_move = None
        self.current_color = WHITE

    def __getitem__(self, position):
        """ Access the board position 
        Usage: board[(x, y)]
        """
        if not self.valid(position):
            return None
        return self.board_data[position[0]][position[1]]

    def add(self, piece):
        """ Add piece to the board.
        This is called in the creation of Piece.
        """
        if not piece:
            return
        if piece.__class__ == King:
            self.kings[piece.color] = piece
        self.board_data[piece.x][piece.y] = piece
        self.pieces[piece.color].append(piece)

    def remove(self, position):
        """ Remove piece from board. """
        piece = self[position]
        if piece:
            self.board_data[piece.x][piece.y] = None
            self.pieces[piece.color].remove(piece)


    def valid(self, position):
        """ Checks if position tuple is inside the board """
        return 0 <= position[0] < 8 and 0 <= position[1] < 8


    def hindered(self, color):
        """ Returns the hindered position by a color """
        result = set()
        for piece in self.pieces[color]:
            result = result.union(piece.possible_moves(hindered=False))
        return result

    def physically_move(self, piece, new_position):
        """ Move a piece to new_position """
        old_piece = self[new_position]
        self.board_data[piece.x][piece.y] = None
        piece.has_moved = True
        self.remove(new_position)
        piece.position = new_position
        self.board_data[piece.x][piece.y] = piece
        return old_piece

    def current_king(self):
        return self.kings[self.current_color]

    def move(self, original_position, new_position):
        """ Move a piece from original_position to new_position 
        Returns False if the movement ins't valid
        Returns True, if it is valid
        Returns CHECK, if it is check
        """
        if (not self.valid(original_position) or not self.valid(new_position) or
                    original_position == new_position):
            return False
        piece = self[original_position]
        if not piece or piece.color != self.current_color:
            return False
        possible_moves = piece.possible_moves()
        if not new_position in possible_moves:
            return False

        old_piece = self.physically_move(piece, new_position)

        move_type = possible_moves[new_position]

        if move_type not in [QUEENSIDE_CASTLING, KINGSIDE_CASTLING]:
            #ToDO: verificar se teve xeque no current_color, reverter movimento e retornar false
            invalid_check = False
            if invalid_check:
                self.physically_move(piece, original_position)
                self.add(old_piece)
                return False

        if move_type == QUEENSIDE_CASTLING:
            rook = self[(0, original_position[1])]
            self.physically_move(rook, (3, original_position[1]))
        if move_type == KINGSIDE_CASTLING:
            rook = self[(7, original_position[1])]
            self.physically_move(rook, (5, original_position[1]))
        if move_type in (RIGHT_EN_PASSANT, LEFT_EN_PASSANT):
            self.remove((new_position[0], original_position[1]))
        if move_type in PROMOTION:
            color = piece.color
            self.remove(new_position)
            queen = Queen(self, color, new_position[0], new_position[1])
            queen.has_moved = True

        self.last_move = (self.current_color, original_position, new_position)
        self.current_color = next(self.current_color)

        #ToDo: verificar se teve xeque no novo current_color e retornar CHECK
        return CHECK

    def in_check(self):
        king = self.kings[self.current_color]
        check = king.is_hindered()
        return check

    def in_check_mate(self):
        king = self.kings[self.current_color]
        possibilities = king.possible_moves()
        if self.in_check() and len(possibilities) == 0:
            return True
        return False