# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os

from .base import Scene, GameText
from pieces.board import Board
from consts.i18n import *
from consts.colors import BLACK, WHITE
from consts.moves import CHECK
from consts.default import TIMER_CLASS

MARGIN = 28
BORDER = 2

RIGHT_MARGIN = 14

# States
SELECT = 0
PLAY = 1
END = 2

CHECK_COUNTDOWN = 0.5


class Chess(Scene):

    def __init__(self, *args, **kwargs):
        """ConfigMenu constructor. Creates texts and buttons"""
        super(Chess, self).__init__(*args, **kwargs)

        # Load current config
        data = self.load_stored_config()

        # Board Image
        self.board_image = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, 'chess_board.png')))
        max_board_size = min(
            self.game.width - (MARGIN + 2 * BORDER), 
            self.game.height - (MARGIN + 2 * BORDER)
        )
        horizontal = True
        self.square_size = (max_board_size // 8)
        self.board_size = self.square_size * 8
        if self.game.width - self.board_size < 3 * self.square_size:
            max_board_size = min(
                self.game.width - (MARGIN + 2 * BORDER), 
                self.game.height - (MARGIN + 2 * BORDER) - 100
            )
            horizontal = False
            self.square_size = (max_board_size // 8)
            self.board_size = self.square_size * 8
        self.board_image = pygame.transform.scale(self.board_image, (self.board_size, self.board_size)) 

        # Labels
        label_font = pygame.font.SysFont("", 26)
        self.labels = []
        for i, label_text in enumerate(range(1, 9)):
            label = GameText(label_font, str(label_text), True, (128, 128, 128))
            label.rect = self.place_rect(
                label.surface,
                13,
                BORDER + (7 - i) * self.square_size + self.square_size // 2,
            )
            self.labels.append(label)

        for i, label_text in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            label = GameText(label_font, str(label_text), True, (128, 128, 128))
            label.rect = self.place_rect(
                label.surface,
                MARGIN +  2*BORDER + i * self.square_size + self.square_size // 2,
                17 + self.board_size + BORDER,
            )
            self.labels.append(label)

        # Images
        color = {
            WHITE: 'white',
            BLACK: 'black',
        }
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.piece_images = {}
        for piece in pieces:
            white_image = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, "%s_%s.png" % (color[WHITE], piece))))
            black_image = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, "%s_%s.png" % (color[BLACK], piece))))
            self.piece_images["%s_%s" % (WHITE, piece)] = pygame.transform.scale(white_image, 
                (self.square_size, self.square_size)) 
            self.piece_images["%s_%s" % (BLACK, piece)] = pygame.transform.scale(black_image, 
                (self.square_size, self.square_size)) 

        # Pieces / Board
        self.board = Board()

        arrow_down = pygame.image.load(os.path.abspath(os.path.join(self.assets_dir, 'arrow_down.png')))
        arrow_down = pygame.transform.scale(arrow_down, (self.square_size // 2, self.square_size // 2))

        arrow_up = pygame.transform.rotate(arrow_down, 180)
        arrow_left = pygame.transform.rotate(arrow_down, 270)
        arrow_right = pygame.transform.rotate(arrow_down, 90)

        # Times
        time_font = pygame.font.SysFont("", 48)
        self.white_image = self.piece_images['%s_king' % WHITE]
        self.black_image = self.piece_images['%s_king' % BLACK]
        
        self.white_time = GameText(time_font, str("20:00"), True, (128, 128, 128))
        self.black_time = GameText(time_font, str("20:00"), True, (128, 128, 128))

        if horizontal:
            self.white_image_position = (
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN), 
                self.game.height - (MARGIN + 2*BORDER) - self.square_size,
            )
            self.white_time.rect = self.place_rect(
                self.white_time.surface,
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN) + self.square_size + MARGIN + RIGHT_MARGIN, 
                self.game.height - (MARGIN + 2*BORDER) - self.square_size // 2
            )
            self.white_arrow = arrow_down
            self.white_arrow_position = (
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN) + self.square_size // 4, 
                self.game.height - (MARGIN + 2*BORDER) - self.square_size - self.square_size // 2,
            )
            self.black_image_position = (
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN), 
                BORDER,
            )
            self.black_time.rect = self.place_rect(
                self.black_time.surface,
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN) + self.square_size + MARGIN + RIGHT_MARGIN, 
                BORDER + self.square_size // 2,
            )
            self.black_arrow = arrow_up
            self.black_arrow_position = (
                self.board_size + (MARGIN + 2*BORDER + RIGHT_MARGIN) + self.square_size // 4, 
                BORDER + self.square_size,
            )
        else:
            self.white_image_position = (
                self.board_size + (MARGIN + 2*BORDER) - self.square_size, 
                self.board_size + 2*BORDER + MARGIN,
            )
            self.white_time.rect = self.place_rect(
                self.white_time.surface,
                self.board_size + (MARGIN + 2*BORDER) - self.square_size - MARGIN - RIGHT_MARGIN - self.square_size // 2, 
                self.board_size + 2*BORDER + MARGIN + self.square_size // 2,
            )
            self.white_arrow = arrow_right
            self.white_arrow_position = (
                self.board_size + (MARGIN + 2*BORDER) - self.square_size - self.square_size // 2, 
                self.board_size + 2*BORDER + MARGIN + self.square_size // 4,
            )
            self.black_image_position = (
                MARGIN + 2*BORDER, 
                self.board_size + 2*BORDER + MARGIN,
            )
            self.black_time.rect = self.place_rect(
                self.black_time.surface,
                MARGIN + 2*BORDER + self.square_size + MARGIN + RIGHT_MARGIN + self.square_size // 2, 
                self.board_size + 2*BORDER + MARGIN + self.square_size // 2,
            )
            self.black_arrow = arrow_left
            self.black_arrow_position = (
                MARGIN + 2*BORDER + self.square_size, 
                self.board_size + 2*BORDER + MARGIN + self.square_size // 4,
            )

        # Selected
        self.selected = None
        self.fail = None
        self.check = None
        self.state = SELECT

        # Messages
        message_font = pygame.font.SysFont("", 148)
        self.check_message = GameText(message_font, CHECK_MESSAGE, True, (30, 144, 255), style="outline", other_color=(255, 255, 255))
        self.check_message.rect = self.place_rect(
            self.check_message.surface, 
            self.board_size // 2 + MARGIN + BORDER,
            self.board_size // 2 + BORDER,
        )

        self.black_wins_message = GameText(message_font, BLACK_WINS_MESSAGE, True, (50, 50, 50), style="outline", other_color=(255, 255, 255))
        self.black_wins_message.rect = self.place_rect(
            self.black_wins_message.surface, 
            self.board_size // 2 + MARGIN + BORDER,
            self.board_size // 2 + BORDER,
        )

        self.white_wins_message = GameText(message_font, WHITE_WINS_MESSAGE, True, (255, 255, 255), style="outline", other_color=(50, 50, 50))
        self.white_wins_message.rect = self.place_rect(
            self.white_wins_message.surface, 
            self.board_size // 2 + MARGIN + BORDER,
            self.board_size // 2 + BORDER,
        )

        self.countdown = 0

        # Timers
        self.white_timer = TIMER_CLASS[data["option"]](data)
        self.black_timer = TIMER_CLASS[data["option"]](data)
        self.thread_events = [self.white_timer.event, self.black_timer.event]
        
        self.white_timer.start()
        self.black_timer.start()
        self.white_timer.start_turn()

        # Winner
        self.white_wins = False
        self.black_wins = False

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

    def show_winner(self):
        if self.white_wins:
            self.white_wins_message.blit(self.game.screen)
        if self.black_wins:
            self.black_wins_message.blit(self.game.screen)

    def draw_square(self, square, color):
        if square:
            pygame.draw.rect(self.game.screen, color, self.position_rect(square))
            position = self.position_rect(square)
            label = GameText(pygame.font.SysFont("", 26), str(square), True, (128, 128, 128))
            label.rect = self.place_rect(
                label.surface,
                position[0] + self.square_size // 2,
                position[1] + self.square_size // 2,
            )
            label.blit(self.game.screen)
    
    def draw(self, delta_time):
        """Draws Chess game"""
        # Background
        self.game.screen.fill((238, 223, 204))
        # Border
        pygame.draw.rect(self.game.screen, (0, 0, 0), 
            (MARGIN, 0, self.board_size + 2 * BORDER, self.board_size + 2 * BORDER))
        # Chess Board
        self.game.screen.blit(self.board_image, (MARGIN + BORDER, BORDER))
        # Labels
        for label in self.labels:
            label.blit(self.game.screen)
        # Selected
        self.draw_square(self.selected, (0, 223, 0))
        self.draw_square(self.fail, (255, 150, 150))
        self.draw_square(self.check, (204, 153, 255))
        # Pieces
        for color, pieces  in self.board.pieces.items():
            for piece in pieces:
                self.game.screen.blit(self.piece_images['%s_%s'%(piece.color, piece.name())], self.position_rect(piece.position))
        # Times
        self.update_timers()
        self.game.screen.blit(self.white_image, self.white_image_position)
        self.game.screen.blit(self.black_image, self.black_image_position)
        self.white_time.blit(self.game.screen)
        self.black_time.blit(self.game.screen)
        # Arrow
        if self.board.current_color == WHITE:
            self.game.screen.blit(self.white_arrow, self.white_arrow_position)
        else:
            self.game.screen.blit(self.black_arrow, self.black_arrow_position) 
        # Messages
        self.countdown = max(self.countdown - delta_time, 0)
        if self.countdown:
            self.check_message.blit(self.game.screen)
        # Winner
        self.show_winner()

    def position_rect(self, position):
        return (
            MARGIN + BORDER + position[0]*self.square_size, 
            BORDER + (7 - position[1])*self.square_size, 
            self.square_size, 
            self.square_size
        )

    def get_square(self, pos):
        x, y = pos[0] - (MARGIN + BORDER), pos[1] - BORDER
        px, py = x // self.square_size, y // self.square_size
        if 0 > px or px > 7 or 0 > py or py > 7:
            return None
        return (px, 7 - py)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEBUTTONUP:
            if self.state == END:
                return
            square = self.get_square(event.pos)
            if square:
                piece = self.board[square]
                if piece and piece.color == self.board.current_color:
                    self.selected = square
                    self.state = PLAY
                elif self.state == PLAY:
                    self.play_event(square, piece)

    def play_event(self, square, piece):
        movement = self.board.move(self.selected, square)
        self.fail = None
        self.check = None
        if movement:
            self.state = SELECT
            self.selected = None
            status = self.board.status()
            print(status)
            if status == CHECK:
                self.check = self.board.current_king().position
                self.countdown = CHECK_COUNTDOWN
            # Verificar vitória aqui
            if self.board.current_color == BLACK:
                self.white_timer.stop_turn()
                self.black_timer.start_turn()
            else:
                self.white_timer.start_turn()
                self.black_timer.stop_turn()
            
        else:
            self.fail = square


