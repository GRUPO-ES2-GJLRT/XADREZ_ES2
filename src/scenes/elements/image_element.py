# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .game_div import GameDiv, LazyAttribute


class ImageElement(GameDiv):

    image = LazyAttribute("_image")

    def __init__(self, image,
                 x=0, y=0, children=None, condition=None, name=''):
        super(ImageElement, self).__init__(x, y, children, condition, name)
        self.image = image

    def draw_element(self, screen, x=0, y=0):
        if not self.image:
            return
        screen.blit(self.image, (x, y))
