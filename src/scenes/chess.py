# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os

from .base import Scene, GameText
from pieces.board import Board
from locales.i18n import *

MARGIN = 28
BORDER = 2




class Chess(Scene):

    def __init__(self, *args, **kwargs):
        """ConfigMenu constructor. Creates texts and buttons"""
        super(Chess, self).__init__(*args, **kwargs)

        # Board Image
        self.board_image = pygame.image.load(os.path.join(self.assets_dir, 'chess_board.png'))
        max_board_size = min(
            self.game.width - (MARGIN + 2 * BORDER), 
            self.game.height - (MARGIN + 2 * BORDER)
        )
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
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.piece_images = {}
        for piece in pieces:
            white_image = pygame.image.load(os.path.join(self.assets_dir, 'white_%s.png' % piece))
            black_image = pygame.image.load(os.path.join(self.assets_dir, 'black_%s.png' % piece))
            self.piece_images["white_%s" % piece] = pygame.transform.scale(white_image, 
                (self.square_size, self.square_size)) 
            self.piece_images["black_%s" % piece] = pygame.transform.scale(black_image, 
                (self.square_size, self.square_size)) 

        # Pieces / Board
        self.board = Board()

        self.square = None
    
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
        if self.square:
            pygame.draw.rect(self.game.screen, (0, 223, 0), self.position_rect(self.square))
            position = self.position_rect(self.square)
            label = GameText(pygame.font.SysFont("", 26), str(self.square), True, (128, 128, 128))
            label.rect = self.place_rect(
                label.surface,
                position[0] + self.square_size // 2,
                position[1] + self.square_size // 2,
            )
            label.blit(self.game.screen)
        # Pieces
        for color, pieces  in self.board.pieces.items():
            for piece in pieces:
                self.game.screen.blit(self.piece_images['%s_%s'%(piece.color, piece.name())], self.position_rect(piece.position()))



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
            self.square = self.get_square(event.pos)

