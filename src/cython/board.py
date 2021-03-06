import re
from collections import namedtuple

Piece = namedtuple("Piece", "name position color")

#<PyxReplace>#
from constants import (
    # Directions
    E, W, EMPTY,
    # Board
    A8, H1,
    # Pieces
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, PIECE_EMPTY,
    # Colors
    COLOR_EMPTY, WHITE, BLACK,
    # Legal
    LEGAL,
    # Movements
    PAWN_OFFSETS, PIECE_OFFSET, PIECE_OFFSET_SIZE,
    NORMAL, CAPTURE, BIG_PAWN, EN_PASSANT,
    KINGSIDE, QUEENSIDE,
    # Rank
    SECOND_RANK,
    # Value Tables
    PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, ROOK_TABLE,
    QUEEN_TABLE, KING_EARLYGAME_TABLE, KING_ENDGAME_TABLE,
    # Attacked
    ATTACKS, RAYS, SHIFTS,
    # Print
    PRINT_ARRAY, NAMES,
    # Functions
    is_square, is_not_square, rank, next_color
)

from functions import tuple_to_0x88, p0x88_to_tuple, chess_notation_to_0x88
from zobrist import (
    zobrist_pieces,
    zobrist_castling,
    zobrist_color,
    zobrist_en_passant
)

from move import Move
#<EndReplace>#


class Board(object):

    def __init__(self, new_game):
        #<PyxReplace>#
        self.pieces = [0] * 128
        self.colors = [0] * 128
        self.kings = [0] * 2
        self.castling = [0] * 2
        self.pieces_count = [0] * 14
        self.values = [0] * 128
        #<EndReplace>#
        if new_game:
            self.load_fen(
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        else:
            self.clear()

    def clear(self):
        for i in range(128):
            self.pieces[i] = PIECE_EMPTY
            self.colors[i] = COLOR_EMPTY
            self.values[i] = 0
        for i in range(7):
            self.pieces_count[WHITE * 7 + i] = 0
            self.pieces_count[BLACK * 7 + i] = 0

        self.kings[WHITE] = EMPTY
        self.kings[BLACK] = EMPTY
        self.current_color = WHITE
        self.castling[0] = 0
        self.castling[1] = 0
        self.en_passant_square = EMPTY
        self.half_moves = 0
        self.moves = 1
        self.hash = 0
        self.pieces_list = []
        self.last_hash = 0
        self.black_value = 23902
        self.white_value = 23902

    def clone(self):
        result = Board(False)
        for i in range(128):
            result.pieces[i] = self.pieces[i]
            result.colors[i] = self.colors[i]
            result.values[i] = self.values[i]
        for i in range(7):
            result.pieces_count[i] = self.pieces_count[i]
            result.pieces_count[7 + i] = self.pieces_count[7 + i]

        result.kings[WHITE] = self.kings[WHITE]
        result.kings[BLACK] = self.kings[BLACK]
        result.current_color = self.current_color
        result.castling[WHITE] = self.castling[WHITE]
        result.castling[BLACK] = self.castling[BLACK]
        result.en_passant_square = self.en_passant_square
        result.half_moves = self.half_moves
        result.moves = self.moves
        result.hash = self.hash
        result.last_hash = self.last_hash
        result.pieces_list = self.pieces_list
        result.black_value = self.black_value
        result.white_value = self.white_value
        return result

    def add(self, piece, color, square):
        self.pieces[square] = piece
        self.colors[square] = color

        if piece == KING:
            self.kings[color] = square

        self.pieces_count[color * 7 + piece] += 1

        self.hash ^= zobrist_pieces[piece][color][square]

    def remove(self, square):
        piece = self.pieces[square]
        color = self.colors[square]
        if piece:
            self.hash ^= zobrist_pieces[piece][color][square]

            if piece == KING:
                self.kings[color] = PIECE_EMPTY
            self.pieces[square] = PIECE_EMPTY
            self.colors[square] = COLOR_EMPTY
            self.pieces_count[color * 7 + piece] -= 1

    def hindered(self, color):
        result = set()
        attack_moves = self.attack_moves(-1, color)
        for move in attack_moves:
            result.add(
                p0x88_to_tuple(move.destination())
            )
        return result

    def get_value(self):
        self.white_value = 0
        self.black_value = 0
        result = 0
        for i in range(A8, H1 + 1):
            if is_not_square(i):
                i = i + 7
                continue
            result += self.values[i]
            if self.colors[i] == WHITE:
                self.white_value += self.values[i]
            elif self.colors[i] == BLACK:
                self.black_value += -self.values[i]
        return result

    def possible_moves(self, color):
        result = self.generate_moves(LEGAL, EMPTY, color)
        result.sort(reverse=True, key=move_key)
        return result

    def possible_killing_moves(self, color):
        result = set()
        moves = self.generate_moves(LEGAL, EMPTY, color)
        for move in moves:
            if move.get_flags() & (CAPTURE | EN_PASSANT):
                result.add(move)
        return result

    def color(self):
        return self.current_color

    def current_king_position(self):
        return p0x88_to_tuple(self._current_king_position())

    def move(self, original_position, new_position, promotion):
        dest = tuple_to_0x88(new_position)
        moves = self.generate_moves(
            LEGAL,
            tuple_to_0x88(original_position),
            COLOR_EMPTY,
        )

        for move in moves:
            if move.destination() == dest:
                move.set_promotion(promotion)
                move.do_update(self)
                return move
        return False

    def piece_moves(self, position):
        square = tuple_to_0x88(position)
        color = self.colors[square]
        moves = self.generate_moves(
            LEGAL,
            square,
            color,
        )
        return moves

    def piece_attack_moves(self, position):
        square = tuple_to_0x88(position)
        color = self.colors[square]
        moves = self.attack_moves(
            square,
            color,
        )
        return moves

    def at(self, position):
        square = tuple_to_0x88(position)
        color = self.colors[square]
        piece = self.pieces[square]
        if piece == PIECE_EMPTY:
            return None
        result = "white " if color == WHITE else "black "
        result += NAMES[piece]
        return result

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
                    self.values[square] = self.piece_value(PAWN, color, square)
                elif lp == 'n':
                    self.add(KNIGHT, color, square)
                    self.values[square] = self.piece_value(KNIGHT,
                                                           color, square)
                elif lp == 'b':
                    self.add(BISHOP, color, square)
                    self.values[square] = self.piece_value(BISHOP,
                                                           color, square)
                elif lp == 'r':
                    self.add(ROOK, color, square)
                    self.values[square] = self.piece_value(ROOK,
                                                           color, square)
                elif lp == 'q':
                    self.add(QUEEN, color, square)
                    self.values[square] = self.piece_value(QUEEN,
                                                           color, square)
                elif lp == 'k':
                    self.add(KING, color, square)
                    self.values[square] = self.piece_value(KING,
                                                           color, square)
                x += 1

        if tokens[1] == 'w':
            self.current_color = WHITE
        else:
            self.current_color = BLACK
            self.hash ^= zobrist_color

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

        self.hash ^= zobrist_castling[self.castle()]

        if tokens[3] != '-':
            self.en_passant_square = chess_notation_to_0x88(tokens[3])
            self.hash ^= zobrist_en_passant[self.en_passant_square]

        self.half_moves = int(tokens[4])

        self.moves = int(tokens[5])

    def castle(self):
        return (
            (self.castling[WHITE] >> 4 >> 1) | (self.castling[BLACK] >> 2 >> 1)
        )

    def attack_moves(self, square, color):
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

    def generate_moves(self, legal, square, color):
        moves = []
        current = color
        first = A8
        last = H1
        single = 0
        if current == COLOR_EMPTY:
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
            move.do(self)
            if not self.in_check(current):
                legal_moves.append(move)
            #else:
            #    self.display()
            move.undo(self)
        return legal_moves

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

    def in_check(self, color):
        if color == COLOR_EMPTY:
            color = self.current_color
        if self.kings[color] == EMPTY:
            return False
        return self.attacked(self.kings[color], next_color(color))

    def _current_king_position(self):
        return self.kings[self.current_color]

    def display(self):
        print("  a b c d e f g h")
        for irow in range(8):
            s = "%d" % (8 - irow)
            for icol in range(8):
                sq = irow * 16 + icol
                s += " %c" % PRINT_ARRAY[self.colors[sq]][self.pieces[sq]]
            print(s)
        print("  a b c d e f g h\n")

    def display_values(self):
        print("  a      b      c      d      e      f      g      h      ")
        for irow in range(8):
            s = "%d " % (8 - irow)
            for icol in range(8):
                sq = irow * 16 + icol
                num = str(self.values[sq])
                s += "%s%s" % (num, " " * (7 - len(num)))
            print(s)
        print("  a      b      c      d      e      f      g      h      ")

    def status(self, possible_moves):
        if not possible_moves:
            possible_moves = self.generate_moves(LEGAL, EMPTY, COLOR_EMPTY)
        in_check = self.in_check(COLOR_EMPTY)
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
        if self.hash != self.last_hash:
            pieces_list = []

            for i in range(A8, H1 + 1):
                if is_not_square(i):
                    i = i + 7
                    continue

                if (self.pieces[i] == PIECE_EMPTY or
                        self.colors[i] == COLOR_EMPTY):
                    continue

                pieces_list.append(Piece(
                    name=NAMES[self.pieces[i]],
                    position=p0x88_to_tuple(i),
                    color="white" if self.colors[i] == WHITE else "black",
                ))
            self.pieces_list = pieces_list
            self.last_hash = self.hash
        return self.pieces_list

    def get_hash(self):
        return self.hash

    def count(self, color, piece):
        return self.pieces_count[color * 7 + piece]

    def piece_value(self, piece, color, square):
        if color == WHITE:
            mult = 1
        else:
            mult = -1
            square = square ^ 0x77
        if piece == PIECE_EMPTY:
            return 0
        if piece == PAWN:
            return mult * (100 + PAWN_TABLE[square])
        elif piece == KNIGHT:
            return mult * (300 + KNIGHT_TABLE[square])
        elif piece == BISHOP:
            return mult * (301 + BISHOP_TABLE[square])
        elif piece == ROOK:
            return mult * (500 + ROOK_TABLE[square])
        elif piece == QUEEN:
            return mult * (900 + QUEEN_TABLE[square])
        elif piece == KING:
            if self.is_endgame():
                return mult * (20000 + KING_ENDGAME_TABLE[square])
            else:
                return mult * (20000 + KING_EARLYGAME_TABLE[square])

    def is_endgame(self):
        return (
            (self.black_value < 21500 and self.white_value < 21500) or
            (self.black_value < 21000 or self.white_value < 21000)
        )

    def get_pieces_count(self):
        the_sum = 0
        for i in range(14):
            the_sum += self.pieces_count[i]
        return the_sum


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


def move_key(move):
    return move.score()
