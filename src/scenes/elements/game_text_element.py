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
                 redraw=False, topleft=False, top=False,
                 x=0, y=0, children=None, condition=None, name=""):
        super(GameTextElement, self).__init__(x, y, children, condition, name)

        self.font = font.get()
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = None
        self.style = style
        self.topleft = topleft
        self.top = top
        self.other_color = other_color if other_color else self.color
        self._redraw = redraw

        self.redraw()

        rect = self.surface.get_rect()
        self.set_rect_position(rect, self.x, self.y)
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
        self.rect = self.surface.get_rect()
        self.set_rect_position(self.rect, self.x, self.y)

    def set_rect_position(self, rect, x=0, y=0):
        rect.center = (x, y)
        if self.topleft:
            rect.topleft = (x, y)
        if self.top:
            rect.top = y

    def draw_element(self, screen, x=0, y=0):
        if self._redraw:
            self.redraw()
        rect = self.surface.get_rect()
        self.set_rect_position(rect, x, y)
        screen.blit(self.surface, rect.topleft)

    def click_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        self.set_rect_position(rect, x, y)
        if rect.collidepoint(pos):
            return self.click_fn(self)

    def motion_element(self, pos, x=0, y=0):
        rect = self.surface.get_rect()
        self.set_rect_position(rect, x, y)
        self.motion_fn(self, rect.collidepoint(pos))

    def start_x(self):
        return self.rect[0] - self.x

    def start_y(self):
        return self.rect[1] - self.y

    def width(self):
        return max(self.rect[2],
                   super(GameTextElement, self).width())

    def height(self):
        return max(self.rect[3],
                   super(GameTextElement, self).height())
