# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .interface import Interface
from scenes.elements import Font, Image


class MenuInterface(Interface):

    def interface(self):
        self.button_color = (255, 255, 255)
        self.button_hover = (200, 200, 200)
        self.title_color = (200, 150, 0)
        self.title_outline = (255, 222, 173)
        self.main_menu_color = (175, 125, 0, 150)
        self.button_background = (175, 125, 0, 200)
        self.value_color = (100, 200, 255)

        self.title_font = Font(size=lambda: self.game.relative_x(0.15))
        self.menu_font = Font(size=lambda: self.game.relative_x(0.05))
        self.label_font = Font(size=lambda: self.game.relative_x(0.04))

        self.load_images()

    def load_images(self):
        self.background_image = Image(
            'background.jpg',
            lambda: (self.game.width, self.game.height),
        )
        self.transform_images()

    def transform_images(self):
        self.background_image.transform()

    def resize(self):
        self.main_div.call('redraw')
        self.transform_images()
