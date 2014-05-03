import re

from collections import namedtuple

Piece = namedtuple("Piece", "name position color")

cdef extern from 'constants.h':
    # Directions
    enum: N, S, E, W, NN, SS, NE, NW, SE, SW
    enum: EEN, EES, WWN, WWS, NNE, NNW, SSE, SSW
    enum: EMPTY
    # Board
    enum: A8, B8, C8, D8, E8, F8, G8, H8
    enum: A7, B7, C7, D7, E7, F7, G7, H7
    enum: A6, B6, C6, D6, E6, F6, G6, H6
    enum: A5, B5, C5, D5, E5, F5, G5, H5
    enum: A4, B4, C4, D4, E4, F4, G4, H4
    enum: A3, B3, C3, D3, E3, F3, G3, H3
    enum: A2, B2, C2, D2, E2, F2, G2, H2
    enum: A1, B1, C1, D1, E1, F1, G1, H1
    # Pieces
    enum: PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, PIECE_EMPTY
    # Colors
    enum: COLOR_EMPTY, WHITE, BLACK
    # Movements
    int **PAWN_OFFSETS
    int **PIECE_OFFSET
    int *PIECE_OFFSET_SIZE
    enum: NORMAL, CAPTURE, BIG_PAWN, EN_PASSANT, PROMOTION
    enum: KINGSIDE, QUEENSIDE
    # Rank
    int *SECOND_RANK
    # Attacked
    int *ATTACKS
    int *RAYS
    int *SHIFTS
    # Print
    char **PRINT_ARRAY
    char **NAMES

cdef inline int is_square(int x):
    if (x & 0x88):
        return 0
    return 1

cdef inline int is_not_square(int x):
    return (x & 0x88)

cdef inline int rank(int x):
    return 8 - (x >> 4)

cdef inline int col(int x):
    return x & 7

cdef inline chess_notation(int x):
    c = col(x)
    r = rank(x) - 1
    return chr(c + 97) + str(r + 1)

cdef inline int next_color(int color):
    if color == WHITE:
        return BLACK
    return WHITE

cdef class Move:
    cdef public int color
    cdef public int origin
    cdef public int dest
    cdef public int flags
    cdef public int piece
    cdef public int promotion
    cdef public int captured

    # undo move
    cdef public int half_moves
    cdef public int previous_en_passant
    cdef public int white_castling
    cdef public int black_castling

    cdef void create(Move self, Board board, int color, int origin, int dest, int flags, int promotion):
        self.color = color
        self.origin = origin
        self.dest = dest
        self.flags = flags
        self.piece = board.pieces[origin]
        self.captured = PIECE_EMPTY
        self.promotion = PIECE_EMPTY

        self.half_moves = board.half_moves
        self.previous_en_passant = board.en_passant_square
        self.white_castling = board.castling[WHITE]
        self.black_castling = board.castling[BLACK]

        if promotion:
            self.flags = self.flags | PROMOTION
            self.promotion = promotion

        if board.pieces[dest]:
            self.captured = board.pieces[dest]
        elif flags & EN_PASSANT:
            self.captured = PAWN

cdef Move new_move(Board board, int color, int origin, int dest, int flags):
    cdef Move move = Move()
    cdef int rank_dest = rank(dest)
    cdef int promotion = 0
    if board.pieces[origin] == PAWN and (rank_dest == 8 or rank_dest == 1):
        promotion = QUEEN
    move.create(board, color, origin, dest, flags, promotion)
    return move

cdef class Board:
    cdef int[128] pieces
    cdef int[128] colors
    cdef int current_color
    cdef int[2] kings
    cdef int[2] castling
    cdef int half_moves
    cdef int moves
    cdef int en_passant_square

    def __init__(self, new_game=True, clone=False):
        if clone:
            return
        if new_game:
            self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        else:
            self.clear()

    cpdef clear(self):
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

    cpdef Board clone(self):
        cdef Board result = Board(clone=True)
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

    cdef void add(self, int piece, int color, int square):
        self.pieces[square] = piece
        self.colors[square] = color

        if piece == KING:
            self.kings[color] = square

    cdef void remove(self, int square):
        if self.pieces[square] == KING:
            self.kings[self.colors[square]] = PIECE_EMPTY
        self.pieces[square] = PIECE_EMPTY
        self.colors[square] = COLOR_EMPTY

    def hindered(self, color):
        result = set()
        cdef int new_color = WHITE if color == 'white' else BLACK
        attack_moves = self.attack_moves(color=new_color)
        for move in attack_moves:
            result.add(
                self.p0x88_to_tuple(move.dest)
            )
        return result

    def possible_moves(self, color):
        result = set()
        cdef int new_color = WHITE if color == 'white' else BLACK
        moves = self.genenate_moves(legal=1, square=-1, color=new_color)
        for move in moves:
            result.add((
                self.p0x88_to_tuple(move.origin),
                self.p0x88_to_tuple(move.dest)
            ))
        return result

    def possible_killing_moves(self, color):
        result = set()
        cdef int new_color = WHITE if color == 'white' else BLACK
        moves = self.genenate_moves(legal=1, square=-1, color=new_color)
        for move in moves:
            if move.flags & (CAPTURE | EN_PASSANT):
                result.add((
                    self.p0x88_to_tuple(move.origin),
                    self.p0x88_to_tuple(move.dest)
                ))
        return result

    def color(self):
        return self._current_color()

    def current_king_position(self):
        return self.p0x88_to_tuple(self._current_king_position())

    def move(self, original_position, new_position, skip_validation=False):
        cdef int dest = self.tuple_to_0x88(new_position)
        moves = self.genenate_moves(
            legal=1,
            square=self.tuple_to_0x88(original_position)
        )

        for move in moves:
            if move.dest == dest:
                self.do_move(move)
                return True
        return False

    def at(self, position):
        cdef int square = self.tuple_to_0x88(position)
        color, piece = self._at(square)
        if piece == PIECE_EMPTY:
            return None
        result = "white " if color == WHITE else "black "
        result += NAMES[piece]
        return result

    cpdef load_fen(self, fen):
        self.clear()
        tokens = re.compile("\s+").split(fen)
        position = tokens[0]
        cdef int y = 7
        cdef int x = 0
        cdef int square
        cdef int color
        digits = '12345678'
        for piece in position:
            if piece == '/':
                y -= 1
                x = 0
            elif piece == '1': x += 1
            elif piece == '2': x += 2
            elif piece == '3': x += 3
            elif piece == '4': x += 4
            elif piece == '5': x += 5
            elif piece == '6': x += 6
            elif piece == '7': x += 7
            elif piece == '8': x += 8
            else:
                square = (7 - y) * 16 + x
                color = WHITE
                lp = piece.lower()
                if piece == lp:
                    color = BLACK
                if lp == 'p': self.add(PAWN, color, square)
                elif lp == 'n': self.add(KNIGHT, color, square)
                elif lp == 'b': self.add(BISHOP, color, square)
                elif lp == 'r': self.add(ROOK, color, square)
                elif lp == 'q': self.add(QUEEN, color, square)
                elif lp == 'k': self.add(KING, color, square)
                x += 1

        self.current_color = WHITE if tokens[1] == 'w' else BLACK

        if tokens[2] != '-':
            for c in tokens[2]:
                if c == 'K': self.castling[WHITE] |= KINGSIDE
                elif c == 'Q': self.castling[WHITE] |= QUEENSIDE
                elif c == 'k': self.castling[BLACK] |= KINGSIDE
                elif c == 'q': self.castling[BLACK] |= QUEENSIDE

        if tokens[3] != '-':
            self.en_passant_square = self.chess_notation_to_0x88(tokens[3])

        self.half_moves = int(tokens[4])

        self.moves = int(tokens[5])

    cdef int chess_notation_to_0x88(self, cn):
        col = ord(cn[0]) - 97
        row = int(cn[1]) - 1
        return (7 - row) * 16 + col

    cpdef int tuple_to_0x88(self, tuple position):
        col = position[0]
        row = position[1]
        return (7 - row) * 16 + col


    cpdef attack_moves(self, int square=-1, int color=-1):
        moves = []
        cdef int current = color
        cdef int other
        cdef int first = A8
        cdef int last = H1
        cdef int piece
        cdef int offset
        cdef int i
        cdef int j
        if (current == -1):
            current = self.current_color
        other = next_color(current)

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
                        moves.append(
                            new_move(self, current, i, square, CAPTURE))
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
                                new_move(self, current, i, square, NORMAL))
                        else:
                            if self.colors[square] == current:
                                break
                            moves.append(
                                new_move(self, current, i, square, CAPTURE))
                            break
                        # Stop after first move for king and knight
                        if (piece == KING or piece == KNIGHT):
                            break
        return moves

    cpdef genenate_moves(self, int legal=0, int square=-1, int color=-1):
        moves = []
        cdef int current = color
        cdef int other
        cdef int first = A8
        cdef int last = H1
        cdef int single = 0
        cdef int piece
        cdef int offset
        cdef int i
        cdef int j
        cdef int origin
        cdef int dest
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
                    moves.append(new_move(self, current, i, square, NORMAL))
                    # 2 steps forward
                    square = i + PAWN_OFFSETS[current][1]
                    if rank(i) == SECOND_RANK[current] and not self.pieces[square]:
                        moves.append(new_move(self, current, i, square, BIG_PAWN))
                # Captures
                for j in range(2, 4):
                    square = i + PAWN_OFFSETS[current][j]
                    if is_not_square(square):
                        continue
                    if self.pieces[square] and self.colors[square] == other:
                        moves.append(new_move(self, current, i, square, CAPTURE))
                    elif square == self.en_passant_square:
                        moves.append(new_move(self, current, i, square, EN_PASSANT))
            else:
                for j in range(0, PIECE_OFFSET_SIZE[piece]):
                    offset = PIECE_OFFSET[piece][j]
                    square = i
                    while True:
                        square += offset
                        if is_not_square(square):
                            break
                        if not self.pieces[square]:
                            moves.append(new_move(self, current, i, square, NORMAL))
                        else:
                            if self.colors[square] == current:
                                break
                            moves.append(new_move(self, current, i, square, CAPTURE))
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
                    moves.append(
                        new_move(self, current, origin, dest, KINGSIDE))
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
                    moves.append(
                        new_move(self, current, origin, dest, QUEENSIDE))

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


    cpdef do_move(self, Move move):
        cdef int current = move.color
        cdef int other = next_color(current)
        cdef int piece = self.pieces[move.origin]
        cdef int color = self.colors[move.origin]
        cdef int other_piece = self.pieces[move.dest]
        cdef int origin = move.origin
        cdef int dest = move.dest
        cdef int flags = move.flags
        cdef int castling_origin
        cdef int castling_dest
        self.remove(origin)
        self.remove(dest)
        self.add(piece, color, dest)

        # En passant
        if flags & EN_PASSANT:
            self.remove(dest + (N if current == BLACK else S))

        # Promotion
        if flags & PROMOTION:
            self.remove(dest)
            self.add(move.promotion, color, dest)

        if piece == KING:
            self.kings[current] = dest

            # Castling
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                piece = self.pieces[castling_origin]
                self.remove(castling_origin)
                self.add(piece, color, castling_dest)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                piece = self.pieces[castling_origin]
                self.remove(castling_origin)
                self.add(piece, color, castling_dest)

            self.castling[current] = 0

        # if move rook, disable castling:
        if self.castling[current] and piece == ROOK:
            if current == WHITE:
                if self.castling[WHITE] & KINGSIDE and origin == H1:
                    self.castling[WHITE] ^= KINGSIDE
                elif self.castling[WHITE] & QUEENSIDE and origin == A1:
                    self.castling[WHITE] ^= KINGSIDE
            if current == BLACK:
                if self.castling[BLACK] & KINGSIDE and origin == H7:
                    self.castling[BLACK] ^= KINGSIDE
                elif self.castling[BLACK] & QUEENSIDE and origin == A7:
                    self.castling[BLACK] ^= KINGSIDE

        # if capture rook, disable castling
        if self.castling[other] and other_piece == ROOK:
            if current == WHITE:
                if self.castling[BLACK] & KINGSIDE and dest == H1:
                    self.castling[BLACK] ^= KINGSIDE
                elif self.castling[BLACK] & QUEENSIDE and dest == A1:
                    self.castling[BLACK] ^= KINGSIDE
            if current == BLACK:
                if self.castling[WHITE] & KINGSIDE and dest == H7:
                    self.castling[WHITE] ^= KINGSIDE
                elif self.castling[WHITE] & QUEENSIDE and dest == A7:
                    self.castling[WHITE] ^= KINGSIDE

        # big pawn
        if flags & BIG_PAWN:
            self.en_passant_square = dest + (N if current == BLACK else S)
        else:
            self.en_passant_square = EMPTY

        # Update half move counter
        if piece == PAWN or (flags & (CAPTURE | EN_PASSANT)):
            self.half_moves = 0
        else:
            self.half_moves += 1

        if current == BLACK:
            self.moves += 1

        self.current_color = next_color(current)

    cpdef undo_move(self, Move move):
        cdef int current = move.color
        cdef int other
        cdef int castling_origin
        cdef int castling_dest
        cdef int dest = move.dest
        cdef int origin = move.origin
        cdef int piece = move.piece
        cdef int rook_piece
        cdef int flags = move.flags
        cdef int captured = move.captured

        self.current_color = current

        other = next_color(current)
        if current == BLACK:
            self.moves -= 1

        self.half_moves = move.half_moves
        self.en_passant_square = move.previous_en_passant
        self.castling[WHITE] = move.white_castling
        self.castling[BLACK] = move.black_castling

        if piece == KING:
            self.kings[current] = origin
            if flags & KINGSIDE:
                castling_origin = dest + E
                castling_dest = dest + W
                rook_piece = self.pieces[castling_dest]
                self.remove(castling_dest)
                self.add(rook_piece, current, castling_origin)
            elif flags & QUEENSIDE:
                castling_origin = dest + W + W
                castling_dest = dest + E
                rook_piece = self.pieces[castling_dest]
                self.remove(castling_dest)
                self.add(rook_piece, current, castling_origin)

        self.remove(dest)
        self.add(piece, current, origin)
        if captured:
            if flags & EN_PASSANT:
                self.add(PAWN, other, dest + (N if current == BLACK else S))
            else:
                self.add(captured, other, dest)

    cpdef int attacked(self, int square, int color):
        cdef int diff
        cdef int diff_0x88
        cdef int offset
        cdef int i
        cdef int j
        cdef int blocked
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

    cpdef int in_check(self, int color=-1):
        if color == -1:
            color = self.current_color
        if self.kings[color] == EMPTY:
            return False
        return self.attacked(self.kings[color], next_color(color))

    cpdef _current_king_position(self):
        return self.kings[self.current_color]

    cpdef tuple _at(self, int square):
        return (self.colors[square], self.pieces[square])

    cpdef display(self):
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
        return (col(position), rank(position) - 1)

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



def say_hello_to(name):
    cdef Board board = Board()
    board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    cdef Board clone = board.clone()
    import random
    for i in range(20):
        moves = board.genenate_moves(1, -1)
        board.do_move(random.choice(moves))
        board.display()
    print(len(board.genenate_moves(0, -1)))
    board.display()
    clone.display()