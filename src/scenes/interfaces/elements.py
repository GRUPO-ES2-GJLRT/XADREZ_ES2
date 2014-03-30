# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame
import types


class LazyAttribute(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]()

    def __set__(self, instance, value):
        instance.__dict__[self.name] = (
            value if isinstance(value, types.FunctionType) else lambda: value)

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class GameDiv(object):

    x = LazyAttribute('_x')
    y = LazyAttribute('_y')

    def __init__(self, x=0, y=0, children=None, condition=None, name=""):
        if not children:
            children = []
        if not condition:
            condition = lambda: True
        self.condition = condition
        self.x = x
        self.y = y
        self.children = children
        self.name = name

    def draw(self, screen, x=0, y=0):
        if not self.condition():
            return
        self.draw_element(screen, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.draw(screen, x=self.x + x, y=self.y + y)

    def click(self, pos, x=0, y=0):
        if not self.condition():
            return
        self.click_element(pos, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.click(pos, x=self.x + x, y=self.y + y)

    def motion(self, pos, x=0, y=0):
        if not self.condition():
            return
        self.motion_element(pos, x=self.x + x, y=self.y + y)
        for child in self.children:
            child.motion(pos, x=self.x + x, y=self.y + y)

    def draw_element(self, screen, x=0, y=0):
        pass

    def click_element(self, pos, x=0, y=0):
        pass

    def motion_element(self, pos, x=0, y=0):
        pass


class ImageElement(GameDiv):

    def __init__(self, image,
                 x=0, y=0, children=None, condition=None, name=""):
        super(ImageElement, self).__init__(x, y, children, condition, name)
        self.image = image

    def draw_element(self, screen, x=0, y=0):
        screen.blit(self.image, (x, y))


class RectElement(GameDiv):

    def __init__(self, color, size_x, size_y,
                 x=0, y=0, children=None, condition=None, name=""):
        super(RectElement, self).__init__(x, y, children, condition, name)
        self.color = color
        self.size_x = size_x
        self.size_y = size_y

    def draw_element(self, screen, x=0, y=0):
        pygame.draw.rect(screen, self.color, (x, y, self.size_x, self.size_y))


class GameTextElement(GameDiv):
    def __init__(self, font, text="", color=(0, 0, 0), antialias=True,
                 style="normal", other_color=None, click=None, motion=None,
                 x=0, y=0, children=None, condition=None, name=""):
        super(GameTextElement, self).__init__(x, y, children, condition, name)
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = None
        self.style = style
        self.other_color = other_color if other_color else self.color
        self.redraw()
        rect = self.surface.get_rect()
        rect.center = (x, y)
        self.rect = rect
        if not click:
            click = lambda it: None
        if not motion:
            motion = lambda it, collides: None
        self.click_fn = click
        self.motion_fn = motion

    def hollow(self):
        notcolor = [c ^ 0xFF for c in self.other_color]
        base = self.font.render(self.text, 0, self.other_color, notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = pygame.Surface(size, 16)
        img.fill(notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)
        return img

    def redraw(self):
        if self.style == "hollow":
            self.surface = self.hollow()
        elif self.style == "outline":
            base = self.font.render(self.text, 0, self.color)
            outline = self.hollow()
            img = pygame.Surface(outline.get_size(), 16)
            img.blit(base, (1, 1))
            img.blit(outline, (0, 0))
            img.set_colorkey(0)
            self.surface = img
        else:
            self.surface = self.font.render(self.text,
                                            self.antialias, self.color)

    def draw_element(self, screen, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        screen.blit(self.surface, rect.topleft)

    def click_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        if rect.collidepoint(pos):
            self.click_fn(self)

    def motion_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        self.motion_fn(self, rect.collidepoint(pos))


class ChessElement(GameDiv):
    def position_rect(self, position, x=0, y=0):
        return (
            x + position[0] * self.square_size,
            y + (7 - position[1]) * self.square_size,
            self.square_size,
            self.square_size
        )


class PiecesElement(ChessElement):
    def __init__(self, board, square_size, piece_images,
                 x=0, y=0, children=None, condition=None, name=""):
        super(PiecesElement, self).__init__(x, y, children, condition, name)
        self.board = board
        self.square_size = square_size
        self.piece_images = piece_images

    def draw_element(self, screen, x=0, y=0):
        for color, pieces in self.board.pieces.items():
            for piece in pieces:
                screen.blit(
                    self.piece_images['%s_%s' % (piece.color, piece.name())],
                    self.position_rect(piece.position, x=x, y=y)
                )


class SquareElement(ChessElement):
    def __init__(self, color, square_size, square,
                 x=0, y=0, children=None, condition=None, name=""):
        super(SquareElement, self).__init__(x, y, children, condition, name)
        self.color = color
        self.square = square
        self.square_size = square_size

    def draw_element(self, screen, x=0, y=0):
        square = self.square()
        if square:
            pygame.draw.rect(screen, self.color,
                             self.position_rect(square, x=x, y=y))
