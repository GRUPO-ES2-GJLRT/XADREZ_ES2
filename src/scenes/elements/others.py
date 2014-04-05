# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import os
import pygame


class LazyAttribute(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]()

    def __set__(self, instance, value):
        instance.__dict__[self.name] = (
            value if callable(value) else lambda: value)

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Font(object):

    size = LazyAttribute("_size")

    def __init__(self, name="", size=size):
        self.name = name
        self.size = size
        self.processed = lambda: pygame.font.SysFont(self.name, self.size)

    def get(self):
        return self.processed


class Image(object):

    dimensions = LazyAttribute("_dimensions")

    def __init__(self, image_name, dimensions):
        image_dir = os.path.abspath(
            os.path.join(sys.argv[0], '..', '..', 'assets', image_name))
        self.image = pygame.image.load(image_dir)
        self.dimensions = dimensions
        self.transform()

    def transform(self):
        self.processed = pygame.transform.scale(self.image, self.dimensions)

    def rotate(self, degree):
        return RotatedImage(self, degree)

    def get(self):
        return self.processed


class RotatedImage(Image):

    def __init__(self, image, degree):
        self.image = pygame.transform.rotate(image.image, degree)
        self._dimensions = image._dimensions
        self.transform()
