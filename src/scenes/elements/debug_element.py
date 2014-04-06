# coding: UTF-8
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pygame


def draw_rect(screen, element, x=0, y=0):
    xi = element.start_x() + x + element.x
    yi = element.start_y() + y + element.y
    pygame.draw.lines(
        screen,
        (255, 128, 128),
        False,
        [
            (xi, yi),
            (xi + element.width(), yi),
            (xi + element.width(), yi + element.height()),
            (xi, yi + element.height()),
            (xi, yi),
        ],
        3
    )
