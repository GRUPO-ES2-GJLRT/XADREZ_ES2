# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from pygame import (
    image,
    transform,
    MOUSEBUTTONUP
)

from os import path

from .base import Scene
from pieces.board import Board
from consts.colors import BLACK, WHITE
from consts.moves import CHECK, CHECKMATE, STALEMATE, FIFTY_MOVE
from consts.default import TIMER_CLASS

from .interfaces.chess_interface import ChessInterface, MARGIN, BORDER, RIGHT_MARGIN
# States
SELECT = 0
PLAY = 1
END = 2

CHECK_COUNTDOWN = 0.5

class Chess(Scene, ChessInterface):

    def __init__(self, game, one_player, selected_level, *args, **kwargs):
        """Inicializando o jogo"""
        super(Chess, self).__init__(game, *args, **kwargs)
        # Game Instance
        self.game = game
        # Estimating board size and orientation
        self.calculate_size()
        # Loading images
        self.load_images()
        # Creating the Game Board
        self.board = Board()
        # Loading configurations
        self.config = self.load_stored_config()
        # Loading players
        if one_player:
            from artificial_intelligence import ArtificialIntelligence
            self.ia = ArtificialIntelligence(self.board, selected_level)
        else:
            self.ia = None
        # Marked squares 
        self.selected = None
        self.fail = None
        self.check = None
        # Game states and countdown for check message
        self.countdown = 0
        self.white_wins = False
        self.black_wins = False
        self.draw_state = False
        self.state = SELECT
        # Timers
        self.white_timer = TIMER_CLASS[self.config['option']](self.config)
        self.black_timer = TIMER_CLASS[self.config['option']](self.config)
        self.thread_events = [self.white_timer.event, self.black_timer.event]
        
        self.white_timer.start()
        self.black_timer.start()
        self.white_timer.start_turn()
        # Creating interface
        self.create_interface()

    def calculate_size(self):
        """ Calculates the board size, square size and the orientation. """
        max_board_size = min(
            self.game.width - (MARGIN + 2 * BORDER),
            self.game.height - (MARGIN + 2 * BORDER)
        )

        self.horizontal = True
        self.square_size = (max_board_size // 8)
        self.board_size = self.square_size * 8
        if self.game.width - self.board_size < 3 * self.square_size:
            max_board_size = min(
                self.game.width - (MARGIN + 2 * BORDER),
                self.game.height - (MARGIN + 2 * BORDER) - 100
            )

            self.horizontal = False
            self.square_size = (max_board_size // 8)
            self.board_size = self.square_size * 8
       
    def load_images(self):
        """ Loads images from the assets_dir """
        # Board
        self.board_image = transform.scale(
            image.load(path.join(self.assets_dir, 'chess_board.png')),
            (self.board_size, self.board_size)
        )

        # Pieces
        self.piece_images = {}

        for color in [BLACK, WHITE]:
            for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                self.piece_images["%s_%s" % (color, piece)] = transform.scale(
                    image.load(path.join(self.assets_dir, "%s_%s.png" % (color, piece))),
                    (self.square_size, self.square_size)
                )

        # Arrows
        self.arrow_down = image.load(path.join(self.assets_dir, 'arrow_down.png'))
        self.arrow_down = transform.scale(self.arrow_down, (self.square_size // 2, self.square_size // 2))
        self.arrow_up = transform.rotate(self.arrow_down, 180)
        self.arrow_left = transform.rotate(self.arrow_down, 270)
        self.arrow_right = transform.rotate(self.arrow_down, 90)

    def update_timers(self):
        self.white_time.text = self.white_timer.minutes_to_text()
        self.black_time.text = self.black_timer.minutes_to_text() 
        self.white_time.redraw()
        self.black_time.redraw()
        if self.white_timer.lose:
            self.state = END
            self.black_wins = True
        if self.black_timer.lose:
            self.state = END
            self.white_wins = True
    
    def draw(self, delta_time):
        """Draws Chess game"""
        # Messages
        self.countdown = max(self.countdown - delta_time, 0)
        # Times
        self.update_timers()
        # Background
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
        if self.ia and self.board.current_color == BLACK:
            return

        if event.type == MOUSEBUTTONUP:
            if self.state == END:
                return
            square = self.get_square(event.pos)
            if square:
                piece = self.board[square]
                if piece and piece.color == self.board.current_color:
                    self.selected = square
                    self.state = PLAY
                elif self.state == PLAY:
                    self.play_event(square)

    def play_event(self, square):
        movement = self.board.move(self.selected, square)
        self.fail = None
        self.check = None
        if movement:
            self.state = SELECT
            self.selected = None
            status = self.board.status()
            if status == CHECK:
                self.check = self.board.current_king().position
                self.countdown = CHECK_COUNTDOWN
            elif status == CHECKMATE:
                self.state = END
                if self.board.current_color == BLACK:
                    self.white_wins = True
                else:
                    self.black_wins = True
            elif status in [STALEMATE, FIFTY_MOVE]:
                self.draw_state = True
                self.state = END

            if self.board.current_color == BLACK:
                self.white_timer.stop_turn()
                self.black_timer.start_turn()
                if self.ia:
                    movement = self.ia.play()
                    if movement:
                        status = self.board.status()
                        if status == CHECK:
                            self.check = self.board.current_king().position
                            self.countdown = CHECK_COUNTDOWN
                        elif status == CHECKMATE:
                            self.state = END
                            self.white_wins = True
                        elif status in [STALEMATE, FIFTY_MOVE]:
                            self.draw_state = True
                            self.state = END
            else:
                self.white_timer.start_turn()
                self.black_timer.stop_turn()
            
        else:
            self.fail = square




    
