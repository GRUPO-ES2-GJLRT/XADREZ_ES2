import cython

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
    # Legal
    enum: ILLEGAL, LEGAL
    # Movements
    int **PAWN_OFFSETS
    int **PIECE_OFFSET
    int *PIECE_OFFSET_SIZE
    enum: NORMAL, CAPTURE, BIG_PAWN, EN_PASSANT, PROMOTION
    enum: KINGSIDE, QUEENSIDE
    # Rank
    int *SECOND_RANK
    # Value Tables
    int *PAWN_TABLE,
    int *KNIGHT_TABLE,
    int *BISHOP_TABLE,
    int *ROOK_TABLE,
    int *QUEEN_TABLE,
    int *KING_EARLYGAME_TABLE,
    int *KING_ENDGAME_TABLE,
    # Attacked
    int *ATTACKS
    int *RAYS
    int *SHIFTS
    # Print
    char **PRINT_ARRAY
    char **NAMES

    int is_square(int x)
    int is_not_square(int x)
    int rank(int x)
    int col(int x)
    int next_color(int color)
    unsigned long long rand64()

cdef:
    unsigned long long zobrist_pieces[7][2][128]
    unsigned long long zobrist_color
    unsigned long long zobrist_castling[16]
    unsigned long long zobrist_en_passant[128]


@cython.locals(piece=cython.int, color=cython.int, square=cython.int)
cdef unsigned long long init_zobrist()

cdef class Move(object):
    cdef int color
    cdef int _origin
    cdef int _destination
    cdef int flags
    cdef int piece
    cdef int promotion
    cdef int captured
    cdef int half_moves
    cdef int previous_en_passant
    cdef int previous_hash
    cdef int white_castling
    cdef int black_castling

    @cython.locals(
        update_value=cython.int, current=cython.int, other=cython.int,
        piece=cython.int, color=cython.int, other_piece=cython.int,
        origin=cython.int, dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int,
        square=cython.int, en_passant_square=cython.int
    )
    cpdef do(self, Board board)

    @cython.locals(
        piece=cython.int, color=cython.int,
        origin=cython.int, dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int,
        en_passant_square=cython.int, promotion=cython.int
    )
    cpdef do_update(self, Board board)

    @cython.locals(
        current=cython.int, other=cython.int, piece=cython.int,
        captured=cython.int, rook_piece=cython.int, origin=cython.int,
        dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int,
        en_passant_square=cython.int
    )
    cpdef undo(self, Board board)

    @cython.locals(
        color=cython.int, other=cython.int, piece=cython.int,
        captured=cython.int, rook_piece=cython.int, origin=cython.int,
        dest=cython.int, flags=cython.int,
        castling_origin=cython.int, castling_dest=cython.int,
        en_passant_square=cython.int
    )
    cpdef undo_update(self, Board board)

    cpdef int origin(self)

    cpdef int destination(self)

    cdef int castle(self)

    cpdef tuple tuple(self)

    cpdef int score(self)

    cpdef int get_flags(self)

    cpdef readable(self)


cdef class Board:
    cdef int pieces[128]
    cdef int colors[128]
    cdef int values[128]
    cdef int current_color
    cdef int kings[2]
    cdef int castling[2]
    cdef int half_moves
    cdef int moves
    cdef int en_passant_square
    cdef unsigned long long hash
    cdef list pieces_list
    cdef unsigned long long last_hash
    cdef int pieces_count[14]

    @cython.locals(i=cython.int)
    cpdef clear(self)

    @cython.locals(result=Board, i=cython.int)
    cpdef Board clone(self)

    @cython.locals(update_value=cython.int)
    cdef void add(self, int piece, int color, int square)

    @cython.locals(piece=cython.int, color=cython.int, update_value=cython.int)
    cdef void remove(self, int square)

    cpdef set hindered(self, int color)

    @cython.locals(result=cython.int, i=cython.int)
    cpdef int get_value(self)

    cpdef list possible_moves(self, int color)

    cpdef list possible_killing_moves(self, int color)

    cpdef int color(self)

    cpdef tuple current_king_position(self)

    @cython.locals(dest=cython.int)
    cpdef move(self, tuple original_position, tuple new_position)

    @cython.locals(dest=cython.int, square=cython.int)
    cpdef list piece_moves(self, tuple position)

    @cython.locals(square=cython.int, color=cython.int, piece=cython.int)
    cpdef at(self, tuple position)

    @cython.locals(
        x=cython.int, y=cython.int, square=cython.int, color=cython.int,
    )
    cpdef load_fen(self, fen)

    cdef int castle(self)

    @cython.locals(
        current=cython.int, other=cython.int, first=cython.int,
        last=cython.int, piece=cython.int, offset=cython.int,
        i=cython.int, j=cython.int
    )
    cdef list attack_moves(self, int square, int color)

    @cython.locals(
        current=cython.int, other=cython.int, first=cython.int,
        last=cython.int, single=cython.int, piece=cython.int,
        offset=cython.int, i=cython.int, j=cython.int,
        origin=cython.int, dest=cython.int
    )
    cdef list generate_moves(self, int legal, int square, int color)

    @cython.locals(
        diff=cython.int, diff_0x88=cython.int, blocked=cython.int,
        offset=cython.int, i=cython.int, j=cython.int,
    )
    cdef int attacked(self, int square, int color)

    cpdef int in_check(self, int color)

    cpdef int _current_king_position(self)

    @cython.locals(irow=cython.int, icol=cython.int, sq=cython.int)
    cpdef display(self)

    @cython.locals(irow=cython.int, icol=cython.int, sq=cython.int)
    cpdef display_values(self)

    cpdef status(self, list possible_moves)

    @cython.locals(i=cython.int)
    cpdef list get_pieces(self)

    cpdef unsigned long long get_hash(self)

    cpdef int count(self, int color, int piece)

    @cython.locals(mult=cython.int)
    cdef int piece_value(self, int piece, int color, int square)

    cdef int is_endgame(self)

    @cython.locals(i=cython.int, the_sum=cython.int)
    cpdef int get_pieces_count(self)


cdef tuple p0x88_to_tuple(int position)

cdef int tuple_to_0x88(tuple position)

@cython.locals(icol=cython.int, irow=cython.int)
cdef int chess_notation_to_0x88(cn)

@cython.locals(icol=cython.int, irow=cython.int)
cdef p0x88_to_chess_notation(int x)


cpdef int move_key(Move move)