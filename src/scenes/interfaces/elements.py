import pygame

from ..base import GameText

class GameDiv(object):

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

    def draw_element(self, screen, x=0, y=0):
        pass


class ImageElement(GameDiv):

    def __init__(self, image, x=0, y=0, children=None, condition=None, name=""):
        super(ImageElement, self).__init__(x, y, children, condition, name)
        self.image = image

    def draw_element(self, screen, x=0, y=0):
        screen.blit(self.image, (x, y))


class RectElement(GameDiv):

    def __init__(self, color, size_x, size_y, x=0, y=0, children=None, condition=None, name=""):
        super(RectElement, self).__init__(x, y, children, condition, name)
        self.color = color
        self.size_x = size_x
        self.size_y = size_y

    def draw_element(self, screen, x=0, y=0):
        pygame.draw.rect(screen, self.color, (x, y, self.size_x, self.size_y))


class GameTextElement(GameDiv, GameText):
    def __init__(self, font, text, antialias, color, rect=None, style="normal", other_color=None, x=0, y=0, children=None, condition=None, name=""):
        GameDiv.__init__(self, x, y, children, condition, name)
        GameText.__init__(self, font, text, antialias, color, rect=rect, style=style, other_color=other_color)

    def draw_element(self, screen, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        screen.blit(self.surface, rect.topleft)


class ChessElement(GameDiv):
    def position_rect(self, position, x=0, y=0):
        return (
            x + position[0]*self.square_size, 
            y + (7 - position[1])*self.square_size, 
            self.square_size, 
            self.square_size
        )


class PiecesElement(ChessElement):
    def __init__(self, board, square_size, piece_images, x=0, y=0, children=None, condition=None, name=""):
        super(PiecesElement, self).__init__(x, y, children, condition, name)
        self.board = board
        self.square_size = square_size
        self.piece_images = piece_images

    def draw_element(self, screen, x=0, y=0):
        for color, pieces  in self.board.pieces.items():
            for piece in pieces:
                screen.blit(
                    self.piece_images['%s_%s'%(piece.color, piece.name())], 
                    self.position_rect(piece.position, x=x, y=y)
                )


class SquareElement(ChessElement):
    def __init__(self, color, square_size, square, x=0, y=0, children=None, condition=None, name=""):
        super(SquareElement, self).__init__(x, y, children, condition, name)
        self.color = color
        self.square = square
        self.square_size = square_size

    def draw_element(self, screen, x=0, y=0):
        square = self.square()
        if square:
            pygame.draw.rect(screen, self.color, self.position_rect(square, x=x, y=y))