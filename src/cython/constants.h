#ifndef CHESS_CONSTANTS_H
#define CHESS_CONSTANTS_H

/* if you edit this file, remember to edit the constants.h */

/* Movement directions */

#define N -16
#define S 16
#define E 1
#define W -1

#define NE -15
#define SW 15
#define NW -17
#define SE 17

#define NN -32
#define SS 32

#define EES 18
#define EEN -14
#define WWS 14
#define WWN -18
#define NNE -31
#define NNW -33
#define SSE 33
#define SSW 31


/* 0x88 board positions */

#define A8 0
#define B8 1
#define C8 2
#define D8 3
#define E8 4
#define F8 5
#define G8 6
#define H8 7

#define A7 16
#define B7 17
#define C7 18
#define D7 19
#define E7 20
#define F7 21
#define G7 22
#define H7 23

#define A6 32
#define B6 33
#define C6 34
#define D6 35
#define E6 36
#define F6 37
#define G6 38
#define H6 39

#define A5 48
#define B5 49
#define C5 50
#define D5 51
#define E5 52
#define F5 53
#define G5 54
#define H5 55

#define A4 64
#define B4 65
#define C4 66
#define D4 67
#define E4 68
#define F4 69
#define G4 70
#define H4 71

#define A3 80
#define B3 81
#define C3 82
#define D3 83
#define E3 84
#define F3 85
#define G3 86
#define H3 87

#define A2 96
#define B2 97
#define C2 98
#define D2 99
#define E2 100
#define F2 101
#define G2 102
#define H2 103

#define A1 112
#define B1 113
#define C1 114
#define D1 115
#define E1 116
#define F1 117
#define G1 118
#define H1 119

#define EMPTY -1

/* Pieces */

#define PAWN 1
#define KNIGHT 2
#define BISHOP 3
#define ROOK 4
#define QUEEN 5
#define KING 6

#define PIECE_EMPTY 0

/* COLOR */

#define COLOR_EMPTY 2
#define WHITE 0
#define BLACK 1

/* Piece movements */

const int PAWN_OFFSETS[2][4] = {
	{N, NN, NE, NW},
	{S, SS, SW, SE}
};

const int PIECE_OFFSET[7][8] = {
	{0, 0, 0, 0, 0, 0, 0, 0}, // EMPTY
	{N, NN, NE, NW, 0, 0, 0, 0}, //PAWN
	{WWS, SSW, SSE, EES, EEN, NNE, NNW, WWN}, // Knight
	{SW, SE, NE, NW, 0, 0, 0, 0}, // Bishop
	{S, E, N, W, 0, 0, 0, 0}, // Rook
	{SW, S, SE, E, NE, N, NW, W}, // Queen
	{SW, S, SE, E, NE, N, NW, W} // King
};

const int PIECE_OFFSET_SIZE[7] = {0, 4, 8, 4, 4, 8, 8};

#define NORMAL 1
#define CAPTURE 2
#define BIG_PAWN 4
#define EN_PASSANT 8
#define PROMOTION 16
#define KINGSIDE 32
#define QUEENSIDE 64

/* Second Rank */
#define WHITE_SECOND_RANK 1
#define BLACK_SECOND_RANK 6

int SECOND_RANK[2] = {WHITE_SECOND_RANK, BLACK_SECOND_RANK};



/* Print */

char PRINT_ARRAY[3][8] = {
	{0, 'P', 'N', 'B', 'R', 'Q', 'K'},
	{0, 'p', 'n', 'b', 'r', 'q', 'k'},
    { 0 , 0 , 0 , 0 , 0,  0, '.'}
};

char NAMES[7][7] = {
  {'\0', '\0', '\0', '\0', '\0', '\0', '\0'},
  {'p', 'a', 'w', 'n', '\0', '\0', '\0'},
  {'k', 'n', 'i', 'g', 'h', 't', '\0'},
  {'b', 'i', 's', 'h', 'o', 'p', '\0'},
  {'r', 'o', 'o', 'k', '\0', '\0', '\0'},
  {'q', 'u', 'e', 'e', 'n', '\0', '\0'},
  {'k', 'i', 'n', 'g', '\0', '\0', '\0'}
};

/* Attack vectors */

int ATTACKS[240] = {
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
};

int RAYS[240] = {
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
};

int SHIFTS[7] = {0, 0, 1, 2, 3, 4, 5};

/* Functions */
inline int is_square(int x) {
	if (x & 0x88)
		return 0;
	return 1;
}

inline int is_not_square(int x) {
	return (x & 0x88);
}

inline int rank(int x) {
	return 7 - (x >> 4);
}

inline int col(int x) {
	return x & 7;
}

inline int next_color(int color) {
	return (color == WHITE) ? BLACK : WHITE;
}


#endif