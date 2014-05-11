#<PyxReplace>#
from constants import col, rank
#<EndReplace>#


def p0x88_to_tuple(position):
    return (col(position), rank(position))


def tuple_to_0x88(position):
    icol = position[0]
    irow = position[1]
    return (7 - irow) * 16 + icol


def chess_notation_to_0x88(cn):
    icol = ord(cn[0]) - 97
    irow = int(cn[1]) - 1
    return (7 - irow) * 16 + icol


def p0x88_to_chess_notation(x):
    icol = col(x)
    irow = rank(x)
    return chr(icol + 97) + str(irow + 1)
