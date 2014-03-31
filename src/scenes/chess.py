# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from pygame import (
    MOUSEBUTTONUP
)

import sys
from .base import Scene
from game_elements import Board, create_player
from game_elements.player import END
from consts.colors import BLACK, WHITE, next
from consts.moves import CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE
from consts.default import TIMER_CLASS
from .interfaces.chess_interface import ChessInterface, MARGIN, BORDER

CHECK_COUNTDOWN = 0.5

GAME_DRAW = 0
WHITE_WINS = 1
BLACK_WINS = 2

WINS = {
    WHITE: WHITE_WINS,
    BLACK: BLACK_WINS,
}


class Chess(Scene, ChessInterface):

    def __init__(self, game, level_white, level_black, *args, **kwargs):
        super(Chess, self).__init__(game, *args, **kwargs)

        self.game = game
        self.board = Board()
        self.white_minutes = lambda: "20:00"
        self.black_minutes = lambda: "20:00"
        self.create_interface()

        # Marked squares
        self.selected = None
        self.fail = None
        self.check = None

        # Game states and countdown for check message
        self.countdown = 0
        self.state = None

        self.initialize_players(level_white, level_black)

    @property
    def current_player(self):
        return self.players[self.board.current_color]

    @property
    def other_player(self):
        return self.players[next(self.board.current_color)]

    def initialize_players(self, level_white, level_black):
        config = self.load_stored_config()

        new_timer = lambda: TIMER_CLASS[config['option']](config)
        white = create_player(WHITE, new_timer(), self, level_white)
        black = create_player(BLACK, new_timer(), self, level_black)
        self.players = {
            WHITE: white,
            BLACK: black,
        }
        self.white_minutes = lambda: white.timer.minutes_to_text()
        self.black_minutes = lambda: black.timer.minutes_to_text()
        self.thread_events = [white.timer.event, black.timer.event]
        self.current_player.start_turn()

    def draw(self, delta_time):
        self.countdown = max(self.countdown - delta_time, 0)
        self.game.screen.fill((238, 223, 204))
        self.main_div.draw(self.game.screen)

    def get_square(self, pos):
        x, y = pos[0] - (MARGIN + BORDER), pos[1] - BORDER
        px, py = x // self.square_size, y // self.square_size
        if 0 > px or px > 7 or 0 > py or py > 7:
            return None
        return (px, 7 - py)

    def event(self, delta_time, event):
        if not self.game.running:
            sys.exit()

        if event.type == MOUSEBUTTONUP:
            if self.current_player.state == END:
                return
            square = self.get_square(event.pos)
            self.current_player.click(square)

    def select(self, square):
        self.selected = square

    def play(self, square):
        self.fail = None
        self.check = None

        movement = self.board.move(self.selected, square)
        if movement:
            self.change_turn()
            self.verify_status(self.board.status())
            return True

        self.fail = square
        return False

    def change_turn(self):
        self.selected = None
        self.fail = None
        self.other_player.end_turn()
        self.current_player.start_turn()

    def verify_status(self, status):
        if status == CHECK:
            self.check = self.board.current_king().position
            self.countdown = CHECK_COUNTDOWN
        elif status == CHECKMATE:
            self.current_player.lose()
        elif status in [STALEMATE, FIFTY_MOVE]:
            for color, player in self.players.items():
                player.state = END
            self.state = GAME_DRAW
            for threaded_event in self.thread_events:
                threaded_event.set()


    def win(self, color):
        for player in self.players.values():
            player.state = END
        self.state = WINS[color]

        for threaded_event in self.thread_events:
            threaded_event.set()

    def resize(self):
        ChessInterface.resize(self)
