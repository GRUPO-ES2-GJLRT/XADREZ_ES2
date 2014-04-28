# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from threading import Thread
from Queue import Queue
from collections import deque

from consts.colors import WHITE, BLACK, next
from consts.moves import (
    LEFT_EN_PASSANT, RIGHT_EN_PASSANT, PROMOTION, NORMAL,
    QUEENSIDE_CASTLING, KINGSIDE_CASTLING,
    CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE, ATTACK, NO_ATTACK, ALL
)

from pieces import (
    Pawn,
    Rook,
    Bishop,
    Queen,
    Knight,
    King
)


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
        self.moves = {
            WHITE: 0,
            BLACK: 0,
        }
        if new_game:
            self.create_pieces()
        self.last_move = None
        self.current_color = WHITE

    def __getitem__(self, position):
        """ Access the board position
        Usage: board[(x, y)]
        """
        if not self.is_valid_position(position):
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

    def create_pieces(self):
        for x in xrange(8):
            Pawn(self, WHITE, x, 1)
            Pawn(self, BLACK, x, 6)

        Rook(self, WHITE, 0, 0)
        Rook(self, WHITE, 7, 0)
        Rook(self, BLACK, 0, 7)
        Rook(self, BLACK, 7, 7)

        Knight(self, WHITE, 1, 0)
        Knight(self, WHITE, 6, 0)
        Knight(self, BLACK, 1, 7)
        Knight(self, BLACK, 6, 7)

        Bishop(self, WHITE, 2, 0)
        Bishop(self, WHITE, 5, 0)
        Bishop(self, BLACK, 2, 7)
        Bishop(self, BLACK, 5, 7)

        Queen(self, WHITE, 3, 0)
        Queen(self, BLACK, 3, 7)

        King(self, WHITE, 4, 0)
        King(self, BLACK, 4, 7)

    def clone(self):
        """ Clones this board """
        new_board = Board(new_game=False)
        new_board.moves = {
            WHITE: self.moves[WHITE],
            BLACK: self.moves[BLACK],
        }
        new_board.last_move = self.last_move
        new_board.current_color = self.current_color
        for piece in self.pieces[WHITE]:
            piece.__class__(new_board, piece.color, piece.x, piece.y)
        for piece in self.pieces[BLACK]:
            piece.__class__(new_board, piece.color, piece.x, piece.y)
        return new_board

    def hindered(self, color):
        """ Returns the hindered position by a color """
        result = set()
        for piece in self.pieces[color]:
            moves = piece.possible_moves(hindered=False)
            result = result.union(moves[1])
            if piece.name() != "pawn":
                result = result.union(moves[0])
        return result

    def optimized_possible_moves(self, color, move_type=ALL):
        queue = Queue()
        threads = []
        moves = []
        attack_moves = []
        no_attack_moves = []

        #Starts a thread for each piece, to get this piece's possible moves
        for piece in self.pieces[color]:
            threads.append(
                Thread(
                    target=piece.optimized_possible_moves, args=(move_type, queue)
                )
            )
            threads[-1].start()

        #Waits until each one of the threads finishes its execution
        #Then gets the return from the thread and puts it in the moves list
        for thread in threads:
            thread.join()
            moves.extend(queue.get())

        #Separates attack moves from no attack moves and then merges them
        #Attack moves come first on the list
        for move in moves:
            if self.is_enemy_position(move[1], color):
                attack_moves.append(move)
            elif self.is_empty_position(move[1]):
                no_attack_moves.append(move)

        return attack_moves + no_attack_moves

    def possible_moves(self, color):
        """ Returns the possible moves positions by a color """
        result = []
        deq = deque()
        for piece in self.pieces[color]:
            moves, attacks = piece.possible_moves()
            deq.appendleft((piece, attacks))
            deq.append((piece, moves))
        while deq:
            piece, moves = deq.popleft()
            for move in moves:
                #nboard = self.clone()
                #nboard.current_color = color
                #if nboard.move(piece.position, move):
                #    result[(piece.position, move)] = nboard
                result.append((piece.position, move))
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
        Returns CHECKMATE, if it is checkmate
        """
        if (not self.is_valid_position(original_position) or
                not self.is_valid_position(new_position) or
                original_position == new_position):
            return False
        piece = self[original_position]
        if not piece or piece.color != self.current_color:
            return False
        possible_moves, pattacks = piece.possible_moves()
        possible_moves.update(pattacks)
        if not new_position in possible_moves:
            return False

        old_piece = self.physically_move(piece, new_position)

        move_type = possible_moves[new_position]

        if move_type not in [QUEENSIDE_CASTLING, KINGSIDE_CASTLING]:
            invalid_check = self.in_check()
            if invalid_check:
                self.physically_move(piece, original_position)
                self.add(old_piece)
                piece.has_moved = False
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

        if piece.__class__ == Pawn or old_piece:
            self.moves = {
                WHITE: 0,
                BLACK: 0,
            }
        else:
            self.moves[self.current_color] += 1

        self.current_color = next(self.current_color)

        return True

    def in_check(self, hindered=None, color=None):
        if not color:
            color = self.current_color
        king = self.kings[color]
        if king:
            in_check, _ = king.get_allowed()
            return in_check
        return False

    def in_checkmate(self, hindered=None, possible_moves=None):
        if possible_moves is None:
            possible_moves = self.possible_moves(self.current_color)
        return self.in_check() and not possible_moves

    def stalemate(self, hindered=None, possible_moves=None):
        if possible_moves is None:
            possible_moves = self.possible_moves(self.current_color)
        return not self.in_check() and not possible_moves

    def status(self, possible_moves=None):
        king = self.current_king()
        king.ignored = True
        hindered = self.hindered(next(self.current_color))
        king.ignored = False
        if not possible_moves:
            possible_moves = self.possible_moves(self.current_color)
        if self.in_checkmate(hindered=hindered, possible_moves=possible_moves):
            return CHECKMATE
        if self.in_check(hindered=hindered):
            return CHECK
        if self.stalemate(hindered=hindered, possible_moves=possible_moves):
            return STALEMATE
        if self.moves[WHITE] >= 50 or self.moves[BLACK] >= 50:
            return FIFTY_MOVE
        return NORMAL

    def has_piece(self, position, color):
        for piece in self.pieces[color]:
            if piece.position == position:
                return True

    def possible_killing_moves(self, color):
        enemy = BLACK if color == WHITE else WHITE
        killing_moves = {}
        for move in self.possible_moves(color):
            if self.has_piece(move[1], enemy):
                killing_moves[move] = None

        return killing_moves

    @staticmethod
    def is_valid_position(position):
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    def is_empty_position(self, position):
        return self[position] is None

    def is_friendly_position(self, position, color):
        return (
            not self.is_empty_position(position) and
            self[position].color == color
        )

    def is_enemy_position(self, position, color):
        return (
            not self.is_empty_position(position) and
            not self[position].color == color
        )

    def hindered_position(self, position, color):
        """ Checks if color is hindering the position.
        If it is, returns all the positions that could block the hinder """
        positions = Allowed()
        if position == (-1, -1):
            return False, positions

        def explore_position(position, lane):
            if not self.is_valid_position(position):
                return 0, None

            piece = self[position]
            if piece and not piece.ignored:
                if piece.color == color:
                    lane.add(position)
                    return 1, piece
                return 0, piece
            lane.add(position)
            return 2, None

        def iterate_lane(rang, cls, dx, dy):
            lane = set()
            for i in rang:
                explore, piece = explore_position(
                    (position[0] + i * dx, position[1] + i * dy),
                    lane
                )
                if explore == 1 and isinstance(piece, cls):
                    positions.union(lane)
                if explore < 2:
                    break

        def iterate_positions(possible_possitions, cls):
            lane = set()
            for pos in possible_possitions:
                if not self.is_valid_position(pos):
                    continue

                piece = self[pos]
                if piece and not piece.ignored:
                    if piece.color == color and isinstance(piece, cls):
                        lane.add(pos)
            if lane:
                positions.union(lane)

        # Bishop / Queen
        # Top Left
        iterate_lane(
            xrange(1, min(position[0], position[1]) + 1), Bishop, -1, -1)

        # Top Right
        iterate_lane(
            xrange(1, min(8 - position[0], position[1]) + 1), Bishop, 1, -1)

        # Bottom Left
        iterate_lane(
            xrange(1, min(position[0], 8 - position[1]) + 1), Bishop, -1, 1)

        # Bottom Right
        iterate_lane(
            xrange(1, min(8 - position[0], 8 - position[1]) + 1), Bishop, 1, 1)

        # Rook / Queen
        # Bottom
        iterate_lane(xrange(1, 8 - position[1]), Rook, 0, 1)

        # Top
        iterate_lane(xrange(1, position[1] + 1), Rook, 0, -1)

        # Left
        iterate_lane(xrange(1, position[0] + 1), Rook, -1, 0)

        # Right
        iterate_lane(xrange(1, 8 - position[0]), Rook, 1, 0)

        # Knight
        pos = position
        iterate_positions([
            (pos[0] - 2, pos[1] - 1), (pos[0] - 2, pos[1] + 1),
            (pos[0] - 1, pos[1] - 2), (pos[0] - 1, pos[1] + 2),
            (pos[0] + 2, pos[1] - 1), (pos[0] + 2, pos[1] + 1),
            (pos[0] + 1, pos[1] - 2), (pos[0] + 1, pos[1] + 2),
        ], Knight)

        # Pawn
        if color == BLACK:
            pawn_positions = [
                (pos[0] - 1, pos[1] + 1), (pos[0] + 1, pos[1] + 1)
            ]
        else:
            pawn_positions = [
                (pos[0] - 1, pos[1] - 1), (pos[0] + 1, pos[1] - 1)
            ]
        iterate_positions(pawn_positions, Pawn)

        # King
        iterate_positions([
            (pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1),
            (pos[0], pos[1] - 1), (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
        ], King)

        if positions.count:
            positions.all = False
            if positions.count > 1:
                positions.allowed = set()
            return True, positions
        return False, positions


class Allowed():

    def __init__(self):
        self.all = True
        self.allowed = set()
        self.count = 0

    def __contains__(self, key):
        if self.all:
            return True
        return key in self.allowed

    def union(self, other):
        self.allowed = self.allowed.union(other)
        self.count += 1
