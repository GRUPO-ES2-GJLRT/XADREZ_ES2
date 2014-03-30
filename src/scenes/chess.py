# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from pygame import (
    MOUSEBUTTONUP
)

from .base import Scene
from game_elements import Board, Player, AIPlayer
from game_elements.player import PLAY, END
from consts.colors import BLACK, WHITE
from consts.moves import CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE
from consts.default import TIMER_CLASS
from .interfaces.chess_interface import ChessInterface, MARGIN, BORDER

CHECK_COUNTDOWN = 0.5

GAME_DRAW = 0
WHITE_WINS = 1
BLACK_WINS = 2


class Chess(Scene, ChessInterface):

    def __init__(self, game, level, *args, **kwargs):
        super(Chess, self).__init__(game, *args, **kwargs)

        self.game = game
        self.board = Board()

        self.create_interface()

        # Marked squares
        self.selected = None
        self.fail = None
        self.check = None

        # Game states and countdown for check message
        self.countdown = 0
        self.state = None

        self.initialize_players(level)

    def initialize_players(self, level):
        config = self.load_stored_config()

        self.white = Player(WHITE, TIMER_CLASS[config['option']](config))

        if level is None:
            self.black = Player(BLACK, TIMER_CLASS[config['option']](config))
        else:
            self.black = AIPlayer(
                BLACK,
                TIMER_CLASS[config['option']](config),
                level,
                self.board
            )

        self.thread_events = [self.white.timer.event, self.black.timer.event]
        self.current_player = self.white
        self.current_player.start_turn()

    def change_turn(self):
        self.selected = None
        self.fail = None
        self.current_player.end_turn()

        self.current_player = (self.black
                               if self.current_player.color == WHITE
                               else self.white)

        self.current_player.start_turn()

    def update_timers(self):
        self.white_time.text = self.white.timer.minutes_to_text()
        self.black_time.text = self.black.timer.minutes_to_text()

        self.white_time.redraw()
        self.black_time.redraw()

        if self.current_player.timer.lose:
            self.current_player.state = END
            if self.current_player.color == WHITE:
                self.state = BLACK_WINS
            else:
                self.state = WHITE_WINS

    def draw(self, delta_time):
        self.countdown = max(self.countdown - delta_time, 0)
        self.update_timers()

        self.game.screen.fill((238, 223, 204))
        self.main_div.draw(self.game.screen)

    def get_square(self, pos):
        x, y = pos[0] - (MARGIN + BORDER), pos[1] - BORDER
        px, py = x // self.square_size, y // self.square_size
        if 0 > px or px > 7 or 0 > py or py > 7:
            return None
        return (px, 7 - py)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if isinstance(self.current_player, AIPlayer):
            return

        if event.type == MOUSEBUTTONUP:
            if self.current_player.state == END:
                return

            square = self.get_square(event.pos)
            if square:
                piece = self.board[square]
                if piece and piece.color == self.current_player.color:
                    self.selected = square
                    self.current_player.state = PLAY
                elif self.current_player.state == PLAY:
                    self.play_event(square)

    def play_event(self, square):
        self.fail = None
        self.check = None

        movement = self.board.move(self.selected, square)
        if movement:
            self.change_turn()
            self.verify_status(self.board.status())

            if isinstance(self.current_player, AIPlayer) and not self.current_player.state == END:
                movement = self.current_player.play()
                if movement:
                    self.change_turn()
                    self.verify_status(self.board.status())
        else:
            self.fail = square

    def verify_status(self, status):
        if status == CHECK:
            self.check = self.board.current_king().position
            self.countdown = CHECK_COUNTDOWN
        elif status == CHECKMATE:
            self.current_player.state = END
            self.state = BLACK_WINS if self.current_player.color == WHITE \
                                    else WHITE_WINS
        elif status in [STALEMATE, FIFTY_MOVE]:
            self.current_player.state = END
            self.state = GAME_DRAW

    def resize(self):
        ChessInterface.resize(self)

