
import re

from collections import namedtuple

Piece = namedtuple("Piece", "name position color")


#<PyxReplace># chess0x88.pyr
# if you edit this section, you may need to edit the chess0x88.pyr

from fake_cython import cython
Board = namedtuple("Board", "none")


from constants import (
    # Directions
    N, S, E, W,
    # NN, SS, NE, NW, SE, SW,
    # EEN, EES, WWN, WWS, NNE, NNW, SSE, SSW,
    EMPTY,
    # Board
    A8,
    A1, A7, H1, H7,
    # A8, B8, C8, D8, E8, F8, G8, H8,
    # A7, B7, C7, D7, E7, F7, G7, H7,
    # A6, B6, C6, D6, E6, F6, G6, H6,
    # A5, B5, C5, D5, E5, F5, G5, H5,
    # A4, B4, C4, D4, E4, F4, G4, H4,
    # A3, B3, C3, D3, E3, F3, G3, H3,
    # A2, B2, C2, D2, E2, F2, G2, H2,
    # A1, B1, C1, D1, E1, F1, G1, H1,
    # Pieces
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, PIECE_EMPTY,
    # Colors
    COLOR_EMPTY, WHITE, BLACK,
    # Movements
    PAWN_OFFSETS,
    PIECE_OFFSET,
    PIECE_OFFSET_SIZE,
    NORMAL, CAPTURE, BIG_PAWN, EN_PASSANT, PROMOTION,
    KINGSIDE, QUEENSIDE,
    # Rank
    SECOND_RANK,
    # Attacked
    ATTACKS,
    RAYS,
    SHIFTS,
    # Print
    PRINT_ARRAY,
    NAMES,
    # Functions
    is_square,
    is_not_square,
    rank,
    col,
    next_color
)


def _set_arrays(board):
    board.pieces = [0] * 128
    board.colors = [0] * 128
    board.kings = [0] * 2
    board.castling = [0] * 2

#<EndReplace>#


def n0x88_to_chess_notation(x):
    c = col(x)
    r = rank(x)
    return chr(c + 97) + str(r + 1)


@cython.cclass
class Move(object):
    cython.declare(
        color=cython.int, _origin=cython.int, _destination=cython.int,
        flags=cython.int, piece=cython.int, promotion=cython.int,
        captured=cython.int, half_moves=cython.int,
        previous_en_passant=cython.int,
        white_castling=cython.int, black_castling=cython.int
    )

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
        self.white_castling = board.castling[WHITE]
        self.black_castling = board.castling[BLACK]

    @cython.ccall
    @cython.locals(
        board=Board, current=cython.int, other=cython.int, piece=cython.int,
        color=cython.int, other_piece=cython.int, origin=cython.int,
        dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int
    )
    def do(self, board):
        current = self.color
        other = next_color(current)
        piece = board.pieces[self._origin]
        color = board.colors[self._origin]
        other_piece = board.pieces[self._destination]
        origin = self._origin
        dest = self._destination
        flags = self.flags
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

        # big pawn
        if flags & BIG_PAWN:
            board.en_passant_square = dest + (N if current == BLACK else S)
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

    @cython.ccall
    @cython.locals(
        board=Board, current=cython.int, other=cython.int, piece=cython.int,
        captured=cython.int, rook_piece=cython.int, origin=cython.int,
        dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int
    )
    def undo(self, board):
        current = self.color
        dest = self._destination
        origin = self._origin
        piece = self.piece
        flags = self.flags
        captured = self.captured

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
                board.add(PAWN, other, dest + (N if current == BLACK else S))
            else:
                board.add(captured, other, dest)

    @cython.ccall
    @cython.returns(cython.int)
    def origin(self):
        return self._origin

    @cython.ccall
    @cython.returns(cython.int)
    def destination(self):
        return self._destination


@cython.cclass
class Board(object):
    cython.declare(
        pieces=cython.int[128], colors=cython.int[128],
        current_color=cython.int, kings=cython.int[2], castling=cython.int[2],
        half_moves=cython.int, moves=cython.int, en_passant_square=cython.int
    )

    def __init__(self, new_game=True, clone=False):
        if not cython.compiled:
            _set_arrays(self)
        if clone:
            return
        if new_game:
            self.load_fen(
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        else:
            self.clear()

    @cython.ccall
    @cython.locals(i=cython.int)
    def clear(self):
        for i in range(128):
            self.pieces[i] = PIECE_EMPTY
            self.colors[i] = COLOR_EMPTY

        self.kings[WHITE] = EMPTY
        self.kings[BLACK] = EMPTY
        self.current_color = WHITE
        self.castling[0] = 0
        self.castling[1] = 0
        self.en_passant_square = EMPTY
        self.half_moves = 0
        self.moves = 1

    @cython.ccall
    @cython.returns(Board)
    @cython.locals(result=Board, i=cython.int)
    def clone(self):
        result = Board(clone=True)
        for i in range(128):
            result.pieces[i] = self.pieces[i]
            result.colors[i] = self.colors[i]

        result.kings[WHITE] = self.kings[WHITE]
        result.kings[BLACK] = self.kings[BLACK]
        result.current_color = self.current_color
        result.castling[WHITE] = self.castling[WHITE]
        result.castling[BLACK] = self.castling[BLACK]
        result.en_passant_square = self.en_passant_square
        result.half_moves = self.half_moves
        result.moves = self.moves
        return result

    @cython.cfunc
    @cython.returns(cython.void)
    @cython.locals(piece=cython.int, color=cython.int, square=cython.int)
    def add(self, piece, color, square):
        self.pieces[square] = piece
        self.colors[square] = color

        if piece == KING:
            self.kings[color] = square

    @cython.cfunc
    @cython.returns(cython.void)
    @cython.locals(square=cython.int)
    def remove(self, square):
        if self.pieces[square] == KING:
            self.kings[self.colors[square]] = PIECE_EMPTY
        self.pieces[square] = PIECE_EMPTY
        self.colors[square] = COLOR_EMPTY

    @cython.ccall
    @cython.locals(new_color=cython.int)
    def hindered(self, color):
        result = set()
        new_color = WHITE if color == 'white' else BLACK
        attack_moves = self.attack_moves(color=new_color)
        for move in attack_moves:
            result.add(
                self.p0x88_to_tuple(move.destination())
            )
        return result

    @cython.ccall
    @cython.locals(new_color=cython.int)
    def possible_moves(self, color):
        result = set()
        new_color = WHITE if color == 'white' else BLACK
        moves = self.genenate_moves(legal=1, square=-1, color=new_color)
        for move in moves:
            result.add((
                self.p0x88_to_tuple(move.origin()),
                self.p0x88_to_tuple(move.destination())
            ))
        return result

    @cython.ccall
    @cython.locals(new_color=cython.int)
    def possible_killing_moves(self, color):
        result = set()
        new_color = WHITE if color == 'white' else BLACK
        moves = self.genenate_moves(legal=1, square=-1, color=new_color)
        for move in moves:
            if move.flags & (CAPTURE | EN_PASSANT):
                result.add((
                    self.p0x88_to_tuple(move.origin()),
                    self.p0x88_to_tuple(move.destination())
                ))
        return result

    def color(self):
        return self._current_color()

    def current_king_position(self):
        return self.p0x88_to_tuple(self._current_king_position())

    @cython.ccall
    @cython.locals(dest=cython.int)
    def move(self, original_position, new_position, skip_validation=False):
        dest = self.tuple_to_0x88(new_position)
        moves = self.genenate_moves(
            legal=1,
            square=self.tuple_to_0x88(original_position)
        )

        for move in moves:
            if move.destination() == dest:
                self.do_move(move)
                return True
        return False

    @cython.ccall
    @cython.locals(square=cython.int)
    def at(self, position):
        square = self.tuple_to_0x88(position)
        color, piece = self._at(square)
        if piece == PIECE_EMPTY:
            return None
        result = "white " if color == WHITE else "black "
        result += NAMES[piece]
        return result

    @cython.ccall
    @cython.locals(
        x=cython.int, y=cython.int, square=cython.int, color=cython.int
    )
    def load_fen(self, fen):
        self.clear()
        tokens = re.compile("\s+").split(fen)
        position = tokens[0]
        y = 7
        x = 0
        for piece in position:
            if piece == '/':
                y -= 1
                x = 0
            elif piece == '1':
                x += 1
            elif piece == '2':
                x += 2
            elif piece == '3':
                x += 3
            elif piece == '4':
                x += 4
            elif piece == '5':
                x += 5
            elif piece == '6':
                x += 6
            elif piece == '7':
                x += 7
            elif piece == '8':
                x += 8
            else:
                square = (7 - y) * 16 + x
                color = WHITE
                lp = piece.lower()
                if piece == lp:
                    color = BLACK
                if lp == 'p':
                    self.add(PAWN, color, square)
                elif lp == 'n':
                    self.add(KNIGHT, color, square)
                elif lp == 'b':
                    self.add(BISHOP, color, square)
                elif lp == 'r':
                    self.add(ROOK, color, square)
                elif lp == 'q':
                    self.add(QUEEN, color, square)
                elif lp == 'k':
                    self.add(KING, color, square)
                x += 1

        self.current_color = WHITE if tokens[1] == 'w' else BLACK

        if tokens[2] != '-':
            for c in tokens[2]:
                if c == 'K':
                    self.castling[WHITE] |= KINGSIDE
                elif c == 'Q':
                    self.castling[WHITE] |= QUEENSIDE
                elif c == 'k':
                    self.castling[BLACK] |= KINGSIDE
                elif c == 'q':
                    self.castling[BLACK] |= QUEENSIDE

        if tokens[3] != '-':
            self.en_passant_square = self.chess_notation_to_0x88(tokens[3])

        self.half_moves = int(tokens[4])

        self.moves = int(tokens[5])

    @cython.ccall
    @cython.returns(cython.int)
    @cython.locals(
        col=cython.int, row=cython.int
    )
    def chess_notation_to_0x88(self, cn):
        col = ord(cn[0]) - 97
        row = int(cn[1]) - 1
        return (7 - row) * 16 + col

    @cython.ccall
    @cython.returns(cython.int)
    @cython.locals(
        position=tuple, col=cython.int, row=cython.int
    )
    def tuple_to_0x88(self, position):
        col = position[0]
        row = position[1]
        return (7 - row) * 16 + col

    @cython.ccall
    @cython.locals(
        square=cython.int, color=cython.int,
        current=cython.int, other=cython.int, first=cython.int,
        last=cython.int, piece=cython.int, offset=cython.int,
        i=cython.int, j=cython.int
    )
    def attack_moves(self, square=-1, color=-1):
        moves = []
        current = color
        first = A8
        last = H1
        if (current == -1):
            current = self.current_color

        if is_square(square):
            first = square
            last = square

        for i in range(first, last + 1):
            if is_not_square(i):
                i = i + 7
                continue
            if self.colors[i] != current:
                continue

            piece = self.pieces[i]
            if piece == PAWN:
                for j in range(2, 4):
                    square = i + PAWN_OFFSETS[current][j]
                    if is_not_square(square):
                        continue
                    if self.colors[square] != current:
                        moves.append(Move(self, current, i, square, CAPTURE))
            else:
                for j in range(0, PIECE_OFFSET_SIZE[piece]):
                    offset = PIECE_OFFSET[piece][j]
                    square = i
                    while True:
                        square += offset
                        if is_not_square(square):
                            break
                        if not self.pieces[square]:
                            moves.append(
                                Move(self, current, i, square, NORMAL))
                        else:
                            if self.colors[square] == current:
                                break
                            moves.append(
                                Move(self, current, i, square, CAPTURE))
                            break
                        # Stop after first move for king and knight
                        if (piece == KING or piece == KNIGHT):
                            break
        return moves

    @cython.ccall
    @cython.locals(
        legal=cython.int, square=cython.int, color=cython.int,
        current=cython.int, other=cython.int, first=cython.int,
        last=cython.int, single=cython.int, piece=cython.int,
        offset=cython.int, i=cython.int, j=cython.int,
        origin=cython.int, dest=cython.int
    )
    def genenate_moves(self, legal=0, square=-1, color=-1):
        moves = []
        current = color
        first = A8
        last = H1
        single = 0
        if current == -1:
            current = self.current_color
        other = next_color(current)

        if is_square(square):
            first = square
            last = square
            single = 1

        for i in range(first, last + 1):
            if is_not_square(i):
                i = i + 7
                continue
            if self.colors[i] != current:
                continue

            piece = self.pieces[i]
            if piece == PAWN:
                # 1 step forward
                square = i + PAWN_OFFSETS[current][0]
                if not self.pieces[square]:
                    moves.append(Move(self, current, i, square, NORMAL))
                    # 2 steps forward
                    square = i + PAWN_OFFSETS[current][1]
                    if (rank(i) == SECOND_RANK[current] and
                            not self.pieces[square]):
                        moves.append(Move(self, current, i, square, BIG_PAWN))
                # Captures
                for j in range(2, 4):
                    square = i + PAWN_OFFSETS[current][j]
                    if is_not_square(square):
                        continue
                    if self.pieces[square] and self.colors[square] == other:
                        moves.append(Move(self, current, i, square, CAPTURE))
                    elif square == self.en_passant_square:
                        moves.append(
                            Move(self, current, i, square, EN_PASSANT))
            else:
                for j in range(0, PIECE_OFFSET_SIZE[piece]):
                    offset = PIECE_OFFSET[piece][j]
                    square = i
                    while True:
                        square += offset
                        if is_not_square(square):
                            break
                        if not self.pieces[square]:
                            moves.append(
                                Move(self, current, i, square, NORMAL))
                        else:
                            if self.colors[square] == current:
                                break
                            moves.append(
                                Move(self, current, i, square, CAPTURE))
                            break
                        # Stop after first for king and knight
                        if (piece == KING or piece == KNIGHT):
                            break

        # Castling
        if ((not single or last == self.kings[current]) and
                self.kings[current] != EMPTY):
            if self.castling[current] & KINGSIDE:
                origin = self.kings[current]
                dest = origin + E + E
                if (not self.pieces[origin + E] and
                        not self.pieces[dest] and
                        not self.attacked(origin, other) and
                        not self.attacked(origin + E, other) and
                        not self.attacked(dest, other)):
                    moves.append(Move(self, current, origin, dest, KINGSIDE))
            if self.castling[current] & QUEENSIDE:
                origin = self.kings[current]
                dest = origin + W + W
                if (not self.pieces[origin + W] and
                        not self.pieces[origin + W + W] and
                        not self.pieces[origin + W + W + W] and
                        not self.pieces[dest] and
                        not self.attacked(origin, other) and
                        not self.attacked(origin + W, other) and
                        not self.attacked(dest, other)):
                    moves.append(Move(self, current, origin, dest, QUEENSIDE))

        if not legal:
            return moves

        legal_moves = []
        for move in moves:
            self.do_move(move)
            if not self.in_check(current):
                legal_moves.append(move)
            #else:
            #    self.display()
            self.undo_move(move)
        return legal_moves

    @cython.ccall
    @cython.locals(move=Move)
    def do_move(self, move):
        move.do(self)

    @cython.ccall
    @cython.locals(move=Move)
    def undo_move(self, move):
        move.undo(self)

    @cython.ccall
    @cython.returns(cython.int)
    @cython.locals(
        square=cython.int, color=cython.int,
        diff=cython.int, diff_0x88=cython.int, blocked=cython.int,
        offset=cython.int, i=cython.int, j=cython.int,
    )
    def attacked(self, square, color):
        for i in range(A8, H1 + 1):
            if is_not_square(i):
                i = i + 7
                continue

            if self.colors[i] != color:
                continue

            piece = self.pieces[i]
            diff = i - square
            diff_0x88 = 0x77 + diff
            if ATTACKS[diff_0x88] & (1 << SHIFTS[piece]):
                if piece == PAWN:
                    if ((diff > 0 and color == WHITE) or
                            (diff <= 0 and color == BLACK)):
                        return True
                    continue

                if piece == KING or piece == KNIGHT:
                    return True

                offset = RAYS[diff_0x88]
                j = i + offset
                blocked = False
                while j != square:
                    if self.pieces[j]:
                        blocked = True
                        break
                    j += offset
                if not blocked:
                    return True
        return False

    @cython.ccall
    @cython.returns(cython.int)
    @cython.locals(color=cython.int)
    def in_check(self, color=-1):
        if color == -1:
            color = self.current_color
        if self.kings[color] == EMPTY:
            return False
        return self.attacked(self.kings[color], next_color(color))

    @cython.ccall
    @cython.returns(cython.int)
    def _current_king_position(self):
        return self.kings[self.current_color]

    @cython.ccall
    @cython.returns(tuple)
    @cython.locals(square=cython.int)
    def _at(self, square):
        return (self.colors[square], self.pieces[square])

    @cython.ccall
    @cython.locals(row=cython.int, col=cython.int, sq=cython.int)
    def display(self):
        print("  a b c d e f g h")
        for row in range(8):
            s = "%d" % (8 - row)
            for col in range(8):
                sq = row * 16 + col
                s += " %c" % PRINT_ARRAY[self.colors[sq]][self.pieces[sq]]
            print(s)
        print("  a b c d e f g h\n")

    def status(self, possible_moves=None):
        if possible_moves is None:
            possible_moves = self.genenate_moves(legal=1)
        in_check = self.in_check()
        if in_check and not possible_moves:
            return "checkmate"
        if in_check:
            return "check"
        if not possible_moves:
            return "stalemate"
        if self.half_moves >= 50:
            return "fifty move"
        return 'normal'

    @cython.locals(i=cython.int)
    def get_pieces(self):
        for i in range(A8, H1 + 1):
            if is_not_square(i):
                i = i + 7
                continue

            if self.colors[i] == COLOR_EMPTY:
                continue

            yield Piece(
                name=NAMES[self.pieces[i]],
                position=self.p0x88_to_tuple(i),
                color="white" if self.colors[i] == WHITE else "black"
            )

    def p0x88_to_tuple(self, position):
        return (col(position), rank(position))

    def _current_color(self):
        return "white" if self.current_color == WHITE else "black"

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
