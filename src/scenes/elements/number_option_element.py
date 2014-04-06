# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .game_div import GameDiv
from .game_text_element import GameTextElement
from consts.i18n import (MINUS, PLUS)


class NumberOptionElement(GameDiv):

    def __init__(self, font, label="", antialias=True,
                 label_color=(0, 0, 0), option_color=(0, 0, 0),
                 style="normal", other_color=None, motion=None,
                 redraw=False, current=None, min_value=0, max_value=999,
                 x=0, y=0, children=None, condition=None, name=""):
        super(NumberOptionElement, self).__init__(
            x, y, children, condition, name)

        if current is None:
            current = (max_value - min_value + 1) // 2

        self.current = current

        def plus(it):
            if self.current < max_value:
                self.value += 1

        def minus(it):
            if self.current > min_value:
                self.value -= 1

        if not motion:
            motion = lambda it, collides: None

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

        self.minus_element = GameTextElement(
            font=font,
            text=MINUS,
            antialias=antialias,
            color=label_color,
            style=style,
            other_color=other_color,
            topleft=True,
            redraw=redraw,
            x=lambda: (self.label_element.x +
                       self.label_element.rect[2]),
            motion=motion,
            click=minus
        )
        self.children.append(self.minus_element)

        self.value_element = GameTextElement(
            font=font,
            text=str(self.current),
            antialias=antialias,
            color=option_color,
            style=style,
            other_color=other_color,
            redraw=redraw,
            top=True,
            x=lambda: (self.label_element.rect[2] +
                       self.minus_element.rect[2] +
                       (font.size * len(str(max_value))) // 4),
        )
        self.children.append(self.value_element)

        self.plus_element = GameTextElement(
            font=font,
            text=PLUS,
            antialias=antialias,
            color=label_color,
            style=style,
            other_color=other_color,
            topleft=True,
            redraw=redraw,
            x=lambda: (self.value_element.x +
                       (font.size * len(str(max_value))) // 4),
            motion=motion,
            click=plus
        )
        self.children.append(self.plus_element)

    @property
    def value(self):
        return self.current

    @value.setter
    def value(self, v):
        self.current = v
        self.value_element.text = str(self.current)
        self.value_element.redraw()
