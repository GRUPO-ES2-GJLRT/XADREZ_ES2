#<PyxReplace>#
from constants import rand64

zobrist_pieces = []
for i in range(7):
    colors = []
    for j in range(2):
        squares = [0] * 128
        colors.append(squares)
    zobrist_pieces.append(colors)

zobrist_color = 0
zobrist_castling = [0] * 16
zobrist_en_passant = [0] * 128
#<EndReplace>#


def init_zobrist():
    for piece in range(7):
        for color in range(2):
            for square in range(128):
                zobrist_pieces[piece][color][square] = rand64()
    zobrist_color = rand64()
    for square in range(16):
        zobrist_castling[square] = rand64()
    for square in range(128):
        zobrist_en_passant[square] = rand64()
    return zobrist_color

zobrist_color = init_zobrist()
