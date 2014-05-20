#<PyxReplace>#
from collections import namedtuple
from utils.fake_cython import cython
Board = namedtuple("Board", "none")

from constants import (
    # Directions
    N, S, E, W,
    EMPTY,
    # Board
    A1, A7, H1, H7,
    # Pieces
    PAWN, ROOK, QUEEN, KING, PIECE_EMPTY,
    # Colors
    WHITE, BLACK,
    # Movements
    CAPTURE, BIG_PAWN, EN_PASSANT, PROMOTION,
    KINGSIDE, QUEENSIDE,
    # Print
    PRINT_ARRAY,
    # Functions
    next_color,
    rank
)

from functions import p0x88_to_tuple, p0x88_to_chess_notation
from zobrist import (
    zobrist_castling,
    zobrist_color,
    zobrist_en_passant
)

#<EndReplace>#


class Move(object):

    @cython.locals(
        board=Board, color=cython.int, origin=cython.int, dest=cython.int,
        flags=cython.int, rank_dest=cython.int, promotion=cython.int
    )
    def __init__(self, board, color, origin, dest, flags):
        rank_dest = rank(dest)
        promotion = 0
        if board.pieces[origin] == PAWN and (rank_dest == 7 or rank_dest == 0):
            promotion = QUEEN
        self.color = color
        self._origin = origin
        self._destination = dest
        self.flags = flags
        self.piece = board.pieces[origin]
        self.promotion = promotion

        if promotion:
            self.flags |= PROMOTION

        if board.pieces[dest]:
            self.captured = board.pieces[dest]
        elif flags & EN_PASSANT:
            self.captured = PAWN
        else:
            self.captured = PIECE_EMPTY

        self.half_moves = board.half_moves
        self.previous_en_passant = board.en_passant_square
        self.previous_hash = board.hash
        self.white_castling = board.castling[WHITE]
        self.black_castling = board.castling[BLACK]

    def do(self, board):
        current = self.color
        other = next_color(current)
        piece = board.pieces[self._origin]
        color = board.colors[self._origin]
        other_piece = board.pieces[self._destination]
        origin = self._origin
        dest = self._destination
        flags = self.flags
        en_passant_square = dest + (N if current == BLACK else S)
        board.remove(origin)
        board.remove(dest)
        board.add(piece, color, dest)

        # En passant
        if flags & EN_PASSANT:
            board.remove(dest + (N if current == BLACK else S))

        # Promotion
        if flags & PROMOTION:
            board.remove(dest)
            board.add(self.promotion, color, dest)

        if piece == KING:
            board.kings[current] = dest

            # Castling
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                piece = board.pieces[castling_origin]
                board.remove(castling_origin)
                board.add(piece, color, castling_dest)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                piece = board.pieces[castling_origin]
                board.remove(castling_origin)
                board.add(piece, color, castling_dest)

            board.castling[current] = 0

        # if move rook, disable castling:
        if board.castling[current] and piece == ROOK:
            if current == WHITE:
                if board.castling[WHITE] & KINGSIDE and origin == H1:
                    board.castling[WHITE] ^= KINGSIDE
                elif board.castling[WHITE] & QUEENSIDE and origin == A1:
                    board.castling[WHITE] ^= KINGSIDE
            if current == BLACK:
                if board.castling[BLACK] & KINGSIDE and origin == H7:
                    board.castling[BLACK] ^= KINGSIDE
                elif board.castling[BLACK] & QUEENSIDE and origin == A7:
                    board.castling[BLACK] ^= KINGSIDE

        # if capture rook, disable castling
        if board.castling[other] and other_piece == ROOK:
            if current == WHITE:
                if board.castling[BLACK] & KINGSIDE and dest == H1:
                    board.castling[BLACK] ^= KINGSIDE
                elif board.castling[BLACK] & QUEENSIDE and dest == A1:
                    board.castling[BLACK] ^= KINGSIDE
            if current == BLACK:
                if board.castling[WHITE] & KINGSIDE and dest == H7:
                    board.castling[WHITE] ^= KINGSIDE
                elif board.castling[WHITE] & QUEENSIDE and dest == A7:
                    board.castling[WHITE] ^= KINGSIDE

        board.hash ^= zobrist_castling[self.castle()]
        board.hash ^= zobrist_castling[board.castle()]

        # big pawn
        if board.en_passant_square != EMPTY:
            board.hash ^= zobrist_en_passant[board.en_passant_square]
        if flags & BIG_PAWN:
            board.en_passant_square = en_passant_square
            board.hash ^= zobrist_en_passant[board.en_passant_square]
        else:
            board.en_passant_square = EMPTY

        # Update half move counter
        if piece == PAWN or (flags & (CAPTURE | EN_PASSANT)):
            board.half_moves = 0
        else:
            board.half_moves += 1

        if current == BLACK:
            board.moves += 1

        board.current_color = next_color(current)
        board.hash ^= zobrist_color

    def do_update(self, board):
        self.do(board)
        piece = self.piece
        color = self.color
        origin = self._origin
        dest = self._destination
        flags = self.flags
        promotion = self.promotion
        en_passant_square = dest + (N if color == BLACK else S)
        board.values[origin] = 0
        board.values[dest] = board.piece_value(piece, color, dest)

        # En passant
        if flags & EN_PASSANT:
            board.values[en_passant_square] = 0

        # Promotion
        if flags & PROMOTION:
            board.values[dest] = board.piece_value(promotion, color, dest)

        # Castling
        if piece == KING:
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                board.values[castling_origin] = 0
                board.values[castling_dest] = board.piece_value(
                    ROOK, color, castling_dest)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                board.values[castling_origin] = 0
                board.values[castling_dest] = board.piece_value(
                    ROOK, color, castling_dest)

    def undo(self, board):
        current = self.color
        dest = self._destination
        origin = self._origin
        piece = self.piece
        flags = self.flags
        captured = self.captured
        en_passant_square = dest + (N if current == BLACK else S)

        board.current_color = current

        other = next_color(current)
        if current == BLACK:
            board.moves -= 1

        board.half_moves = self.half_moves
        board.en_passant_square = self.previous_en_passant
        board.castling[WHITE] = self.white_castling
        board.castling[BLACK] = self.black_castling

        if piece == KING:
            board.kings[current] = origin
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                rook_piece = board.pieces[castling_dest]
                board.remove(castling_dest)
                board.add(rook_piece, current, castling_origin)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                rook_piece = board.pieces[castling_dest]
                board.remove(castling_dest)
                board.add(rook_piece, current, castling_origin)

        board.remove(dest)
        board.add(piece, current, origin)
        if captured:
            if flags & EN_PASSANT:
                board.add(PAWN, other, en_passant_square)
            else:
                board.add(captured, other, dest)

        board.hash = self.previous_hash

    def undo_update(self, board):
        self.undo(board)
        color = self.color
        other = next_color(color)
        dest = self._destination
        origin = self._origin
        piece = self.piece
        flags = self.flags
        captured = self.captured
        en_passant_square = dest + (N if color == BLACK else S)

        # castling
        if piece == KING:
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                board.values[castling_dest] = 0
                board.values[castling_origin] = board.piece_value(
                    ROOK, color, castling_origin)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                board.values[castling_dest] = 0
                board.values[castling_origin] = board.piece_value(
                    ROOK, color, castling_origin)

        board.values[origin] = board.piece_value(piece, color, dest)
        if captured:
            if flags & EN_PASSANT:
                board.values[en_passant_square] = board.piece_value(
                    PAWN, other, en_passant_square)
            else:
                board.values[dest] = board.piece_value(captured, other, dest)
        else:
            board.values[dest] = 0

    def origin(self):
        return self._origin

    def destination(self):
        return self._destination

    def castle(self):
        return (
            (self.white_castling >> 4 >> 1) | (self.black_castling >> 2 >> 1)
        )

    def tuple(self):
        return (
            p0x88_to_tuple(self._origin),
            p0x88_to_tuple(self._destination)
        )

    def score(self):
        return self.captured

    def get_flags(self):
        return self.flags

    def readable(self):
        return "%s%s %c" % (
            p0x88_to_chess_notation(self._origin),
            p0x88_to_chess_notation(self._destination),
            PRINT_ARRAY[self.color][self.piece]
        )
