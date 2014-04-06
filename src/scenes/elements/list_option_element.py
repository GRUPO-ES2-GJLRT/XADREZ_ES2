# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from functools import partial

from .game_div import GameDiv
from .game_text_element import GameTextElement


class ListOptionElement(GameDiv):

    def __init__(self, font, label="", antialias=True,
                 label_color=(0, 0, 0), option_color=(0, 0, 0),
                 style="normal", other_color=None, motion=None, options={},
                 redraw=False, select=None, current=None,
                 x=0, y=0, children=None, condition=None, name=""):
        super(ListOptionElement, self).__init__(
            x, y, children, condition, name)

        self.options = options.items()

        if current is None:
            current = self.options[0][0]

        self.current = current

        if not select:
            select = lambda it, option: None
        if not motion:
            motion = lambda it, collides: None

        def select_fn(it, option):
            self.current = option
            select(it, option)
            return True

        self.label_element = GameTextElement(
            font=font,
            text=label,
            antialias=antialias,
            color=label_color,
            style=style,
            other_color=other_color,
            topleft=True,
            redraw=redraw,
        )
        self.children.append(self.label_element)

        for i, (option, text) in enumerate(self.options):
            next = self.options[(i + 1) % len(options)]
            element = GameTextElement(
                font=font,
                text=text,
                antialias=antialias,
                color=option_color,
                style=style,
                other_color=other_color,
                topleft=True,
                redraw=redraw,
                x=lambda: self.label_element.rect[2],
                motion=motion,
                click=partial(select_fn, option=next[0]),
                condition=partial((lambda o: self.current == o), o=option)
            )
            self.children.append(element)

    def set_option(self, option):
        self.current = option
