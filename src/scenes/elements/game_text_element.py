# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pygame import Surface
from .game_div import GameDiv
from .others import LazyAttribute


class GameTextElement(GameDiv):

    font = LazyAttribute("_font")
    text = LazyAttribute("_text")

    def __init__(self, font, text="", color=(0, 0, 0), antialias=True,
                 style="normal", other_color=None, click=None, motion=None,
                 redraw=False, topleft=False,
                 x=0, y=0, children=None, condition=None, name=""):
        super(GameTextElement, self).__init__(x, y, children, condition, name)

        self.font = font.get()
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = None
        self.style = style
        self.topleft = topleft
        self.other_color = other_color if other_color else self.color
        self._redraw = redraw

        self.redraw()

        rect = self.surface.get_rect()
        rect.center = (self.x, self.y)
        if self.topleft:
            rect.topleft = (self.x, self.y)
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
        if self._redraw:
            self.redraw()
        rect = self.surface.get_rect()
        rect.center = (x, y)
        if self.topleft:
            rect.topleft = (x, y)
        screen.blit(self.surface, rect.topleft)

    def click_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        if self.topleft:
            rect.topleft = (x, y)
        if rect.collidepoint(pos):
            return self.click_fn(self)

    def motion_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (x, y)
        if self.topleft:
            rect.topleft = (x, y)
        self.motion_fn(self, rect.collidepoint(pos))

    def calculate_rect(self, x=0, y=0):
        rect = self.surface.get_rect()
        rect.center = (self.x + x, self.y + y)
        if self.topleft:
            rect.topleft = (self.x + x, self.y + y)
        return rect
