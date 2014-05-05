# if you edit this file, remember to edit the constants.h
import uuid


# Movement directions

N, S, E, W = -16, 16, 1, -1
NE, SW, NW, SE = -15, 15, -17, 17
NN, SS = -32, 32
EES, EEN, WWS, WWN, NNE, NNW, SSE, SSW = 18, -14, 14, -18, -31, -33, 33, 31

# 0x88 board positions

A8, B8, C8, D8, E8, F8, G8, H8 =   0,   1,   2,   3,   4,   5,   6,   7
A7, B7, C7, D7, E7, F7, G7, H7 =  16,  17,  18,  19,  20,  21,  22,  23
A6, B6, C6, D6, E6, F6, G6, H6 =  32,  33,  34,  35,  36,  37,  38,  39
A5, B5, C5, D5, E5, F5, G5, H5 =  48,  49,  50,  51,  52,  53,  54,  55
A4, B4, C4, D4, E4, F4, G4, H4 =  64,  65,  66,  67,  68,  69,  70,  71
A3, B3, C3, D3, E3, F3, G3, H3 =  80,  81,  82,  83,  84,  85,  86,  87
A2, B2, C2, D2, E2, F2, G2, H2 =  96,  97,  98,  99, 100, 101, 102, 103
A1, B1, C1, D1, E1, F1, G1, H1 = 112, 113, 114, 115, 116, 117, 118, 119

EMPTY = -1

# Pieces

PIECE_EMPTY = 0
from consts.pieces import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

# COLOR

from consts.colors import WHITE, BLACK

COLOR_EMPTY = 2

# Piece movements

PAWN_OFFSETS = [
    [N, NN, NE, NW],
    [S, SS, SW, SE]
]

PIECE_OFFSET = [
    [0, 0, 0, 0, 0, 0, 0, 0],                  # EMPTY
    [N, NN, NE, NW, 0, 0, 0, 0],               # PAWN
    [WWS, SSW, SSE, EES, EEN, NNE, NNW, WWN],  # Knight
    [SW, SE, NE, NW, 0, 0, 0, 0],              # Bishop
    [S, E, N, W, 0, 0, 0, 0],                  # Rook
    [SW, S, SE, E, NE, N, NW, W],              # Queen
    [SW, S, SE, E, NE, N, NW, W]               # King
]

PIECE_OFFSET_SIZE = [0, 4, 8, 4, 4, 8, 8]

NORMAL, CAPTURE, BIG_PAWN, EN_PASSANT, PROMOTION = 1, 2, 4, 8, 16
KINGSIDE, QUEENSIDE = 32, 64

# Second Rank

WHITE_SECOND_RANK = 1
BLACK_SECOND_RANK = 6

SECOND_RANK = [WHITE_SECOND_RANK, BLACK_SECOND_RANK]

# Print

PRINT_ARRAY = [
    [0, 'P', 'N', 'B', 'R', 'Q', 'K'],
    [0, 'p', 'n', 'b', 'r', 'q', 'k'],
    [0, 0, 0, 0, 0, 0, '.']
]

NAMES = ["", "pawn", "knight", "bishop", "rook", "queen", "king"]

#Value Tables
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0,
    10, 10, 20, 30, 30, 20, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0,
    5,  5, 10, 25, 25, 10,  5,  5, 0, 0, 0, 0, 0, 0, 0, 0,
    0,  0,  0, 20, 20,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0,
    5, -5, -10,  0,  0, -10, -5,  5, 0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10,  5, 0, 0, 0, 0, 0, 0, 0, 0,
    0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0,
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50, 0, 0, 0, 0, 0, 0, 0, 0,
    -40, -20,  0,  0,  0,  0, -20, -40, 0, 0, 0, 0, 0, 0, 0, 0,
    -30,  0, 10, 15, 15, 10,  0, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30,  5, 15, 20, 20, 15,  5, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30,  0, 15, 20, 20, 15,  0, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30,  5, 10, 15, 15, 10,  5, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -40, - 20,  0,  5,  5,  0, -20, -40, 0, 0, 0, 0, 0, 0, 0, 0,
    -50, -40, -30, -30, -30, -30, -40, -50, 0, 0, 0, 0, 0, 0, 0, 0,
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0,  0,  0,  0,  0,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0,  5, 10, 10,  5,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  5,  5, 10, 10,  5,  5, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0, 10, 10, 10, 10,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10, 10, 10, 10, 10, 10, 10, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  5,  0,  0,  0,  0,  5, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -20, -10, -10, -10, -10, -10, -10, -20, 0, 0, 0, 0, 0, 0, 0, 0,
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10,  5, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  0,  0,  0,  0,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  0,  0,  0,  0,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  0,  0,  0,  0,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  0,  0,  0,  0,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  0,  0,  0,  0,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    0,  0,  0,  5,  5,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0,
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0,  0,  0,  0,  0,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0,  5,  5,  5,  5,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -5,  0,  5,  5,  5,  5,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    0,  0,  5,  5,  5,  5,  0, -5, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  5,  5,  5,  5,  5,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -10,  0,  5,  0,  0,  0,  0, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    -20, -10, -10, -5,  -5, -10, -10, -20, 0, 0, 0, 0, 0, 0, 0, 0,
]

KING_EARLYGAME_TABLE = [
    -30, -40, -40, -50, -50, -40, -40, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -40, -40, -50, -50, -40, -40, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -40, -40, -50, -50, -40, -40, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -40, -40, -50, -50, -40, -40, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -20, -30, -30, -40, -40, -30, -30, -20, 0, 0, 0, 0, 0, 0, 0, 0,
    -10, -20, -20, -20, -20, -20, -20, -10, 0, 0, 0, 0, 0, 0, 0, 0,
    20, 20,  0,  0,  0,  0, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0,
    20, 30, 10,  0,  0, 10, 30, 20, 0, 0, 0, 0, 0, 0, 0, 0,
]

KING_ENDGAME_TABLE = [
    -50, -40, -30, -20, -20, -30, -40, -50, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -20, -10,  0,  0, -10, -20, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -10, 20, 30, 30, 20, -10, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -10, 30, 40, 40, 30, -10, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -10, 30, 40, 40, 30, -10, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -10, 20, 30, 30, 20, -10, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -30, -30,  0,  0,  0,  0, -30, -30, 0, 0, 0, 0, 0, 0, 0, 0,
    -50, -30, -30, -30, -30, -30, -30, -50, 0, 0, 0, 0, 0, 0, 0, 0,
]


# Attack vectors

ATTACKS = [
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
    24,24,24,24,24,24,56,  0, 56,24,24,24,24,24,24, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20
]

RAYS = [
     17,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0, 15, 0,
      0, 17,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0, 15,  0, 0,
      0,  0, 17,  0,  0,  0,  0, 16,  0,  0,  0,  0, 15,  0,  0, 0,
      0,  0,  0, 17,  0,  0,  0, 16,  0,  0,  0, 15,  0,  0,  0, 0,
      0,  0,  0,  0, 17,  0,  0, 16,  0,  0, 15,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0, 17,  0, 16,  0, 15,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0,  0, 17, 16, 15,  0,  0,  0,  0,  0,  0, 0,
      1,  1,  1,  1,  1,  1,  1,  0, -1, -1,  -1,-1, -1, -1, -1, 0,
      0,  0,  0,  0,  0,  0,-15,-16,-17,  0,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0,-15,  0,-16,  0,-17,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,-15,  0,  0,-16,  0,  0,-17,  0,  0,  0,  0, 0,
      0,  0,  0,-15,  0,  0,  0,-16,  0,  0,  0,-17,  0,  0,  0, 0,
      0,  0,-15,  0,  0,  0,  0,-16,  0,  0,  0,  0,-17,  0,  0, 0,
      0,-15,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,-17,  0, 0,
    -15,  0,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,  0,-17
]

SHIFTS = [0, 0, 1, 2, 3, 4, 5]

# Functions


def is_square(x):
    if x & 0x88:
        return 0
    return 1


def is_not_square(x):
    return (x & 0x88)


def rank(x):
    return 7 - (x >> 4)


def col(x):
    return x & 7


def next_color(color):
    return BLACK if color == WHITE else WHITE


def rand64():
    return uuid.uuid4().int & (1 << 64) - 1
