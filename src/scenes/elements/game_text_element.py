# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pygame import Surface
from.game_div import GameDiv


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
        img = Surface(size, 16)
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
            img = Surface(outline.get_size(), 16)
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
