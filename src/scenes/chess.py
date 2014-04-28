# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from pygame import (
    MOUSEBUTTONUP,
    MOUSEMOTION,
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_t,
    K_DOWN,
    K_UP,
    K_LEFT,
    K_RIGHT,
)

import sys
from .base import Scene
from game_elements import Board, create_player, InputPlayer
from game_elements.player import END
from consts.colors import BLACK, WHITE, next
from consts.moves import CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE
from consts.default import TIMER_CLASS, FIFTY_MOVE_OPTIONS
from .interfaces.chess_interface import ChessInterface, MARGIN, BORDER
from .pause_menu import PauseMenu
from .end_menu import EndMenu
from .dialog import Dialog
from consts.i18n import CONFIRM_DRAW

CHECK_COUNTDOWN = 0.5

GAME_DRAW = 0
WHITE_WINS = 1
BLACK_WINS = 2
PAUSE = 3

END_GAME = [GAME_DRAW, WHITE_WINS, BLACK_WINS]

WINS = {
    WHITE: WHITE_WINS,
    BLACK: BLACK_WINS,
}

SCROLL_SPEED = 50


class Chess(Scene, ChessInterface):

    def __init__(self, game, level_white, level_black, *args, **kwargs):
        super(Chess, self).__init__(game, *args, **kwargs)

        self.game = game
        self.white_minutes = lambda: "20:00"
        self.black_minutes = lambda: "20:00"
        self.define_clicks()
        self.create_interface()

        self.level_white = level_white
        self.level_black = level_black

        self.should_draw_tree = False
        self.view = [0, 0]
        self.scrolling = None

        self.new_game()

    @property
    def current_player(self):
        return self.players[self.board.current_color]

    @property
    def other_player(self):
        return self.players[next(self.board.current_color)]

    @property
    def human_player(self):
        return isinstance(self.current_player, InputPlayer)

    def define_clicks(self):
        def draw_click(it):
            if self.human_player:
                self.other_player.confirm_draw()

        def resign_click(it):
            if self.human_player:
                self.current_player.lose()

        def motion(it, collides):
            if not self.human_player or not collides:
                it.color = self.button_color
            else:
                it.color = self.button_hover
            it.redraw()

        self.draw_click = draw_click
        self.resign_click = resign_click
        self.motion = motion

    def new_game(self):
        self.free_events()
        self.config = self.load_stored_config()
        self.fifty_move = self.config['fifty_move']
        self.board = Board()
        # Marked squares
        self.selected = None
        self.fail = None
        self.check = None

        # Game states and countdown for check message
        self.countdown = 0
        self.denied_countdown = 0
        self.state = None

        self.initialize_players()
        self.game.scene = self

    def initialize_players(self):
        new_timer = lambda: TIMER_CLASS[self.config['timer']](self.config)
        white = create_player(WHITE, new_timer(), self, self.level_white)
        black = create_player(BLACK, new_timer(), self, self.level_black)
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
        self.denied_countdown = max(self.denied_countdown - delta_time, 0)
        self.game.screen.fill((238, 223, 204))
        if not self.should_draw_tree:
            self.main_div.draw(self.game.screen)
        else:
            if self.scrolling == K_DOWN:
                self.view[1] += SCROLL_SPEED
            if self.scrolling == K_UP:
                self.view[1] -= SCROLL_SPEED
            if self.scrolling == K_LEFT:
                self.view[0] -= SCROLL_SPEED
            if self.scrolling == K_RIGHT:
                self.view[0] += SCROLL_SPEED
            self.tree.draw(self.game.screen,
                           x=-self.view[0], y=-self.view[1])

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
            self.main_div.click(event.pos)
        elif event.type == MOUSEMOTION:
            self.main_div.motion(event.pos)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.pause()
            if event.key == K_t:
                self.should_draw_tree = not self.should_draw_tree
            if event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                self.scrolling = event.key
        if event.type == KEYUP:
            self.scrolling = None

    def select(self, square):
        self.selected = square

    def play(self, square, skip_validation=False):
        self.fail = None
        self.check = None

        movement = self.board.move(self.selected, square, skip_validation)
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
        elif status == STALEMATE:
            self.end_game(GAME_DRAW)
        elif status == FIFTY_MOVE:
            if self.fifty_move == FIFTY_MOVE_OPTIONS["auto"]:
                self.end_game(GAME_DRAW)

    def win(self, color):
        self.end_game(WINS[color])

    def end_game(self, state):
        for player in self.players.values():
            player.state = END
        self.state = state
        for threaded_event in self.thread_events:
            threaded_event.set()
        self.game.scene = EndMenu(game=self.game, chess=self)

    def resize(self):
        ChessInterface.resize(self)

    def pause(self):
        self.previous_state = self.state
        self.state = PAUSE
        self.current_player.pause_turn()
        self.other_player.pause_turn()
        self.game.scene = PauseMenu(game=self.game, chess=self)

    def resume(self):
        self.state = self.previous_state
        self.game.scene = self
        self.current_player.resume_turn()

    def confirm_draw_dialog(self, player):
        if (self.fifty_move == FIFTY_MOVE_OPTIONS["button"] and
                self.board.status() == FIFTY_MOVE):
            self.end_game(GAME_DRAW)
            return

        def yes_click(it):
            self.end_game(GAME_DRAW)

        def no_click(it):
            self.deny_draw(player)
            self.resume()

        self.pause()
        self.game.scene = Dialog(
            game=self.game,
            chess=self,
            message=CONFIRM_DRAW,
            yes_click=yes_click,
            no_click=no_click
        )

    def deny_draw(self, player):
        self.denied_countdown = CHECK_COUNTDOWN
