import pygame

from .game_div import GameDiv
from .others import LazyAttribute


def AAfilledRoundedRect(surface, rect, color, radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


class ButtonGroup(GameDiv):

    define_rect = LazyAttribute("_define_rect")
    extra_padding = LazyAttribute("_extra_padding")

    def __init__(self, color=(255, 255, 255, 125), radius=0.1, padding=5,
                 extra_padding=[0, 0, 0, 0], define_rect=False,
                 x=0, y=0, children=None, condition=None, name=""):
        super(ButtonGroup, self).__init__(x, y, children, condition, name)
        self.color = color
        self.radius = radius
        self.padding = padding
        self.extra_padding = extra_padding
        self.define_rect = define_rect

    def draw_element(self, screen, x=0, y=0):
        rect = [self.start_x() + x - self.x, self.start_y() + y - self.y,
                self.width(), self.height()]

        AAfilledRoundedRect(screen, rect, self.color, self.radius)

    def start_x(self):
        if not self.define_rect:
            return (super(ButtonGroup, self).start_x()
                    - self.padding - self.extra_padding[0])
        return self.x + self.define_rect[0]

    def start_y(self):
        if not self.define_rect:
            return (super(ButtonGroup, self).start_y()
                    - self.padding - self.extra_padding[1])
        return self.y + self.define_rect[1]

    def width(self):
        if not self.define_rect:
            return (super(ButtonGroup, self).width()
                    + self.padding + self.extra_padding[0]
                    + self.extra_padding[2])
        return self.define_rect[2]

    def height(self):
        if not self.define_rect:
            return (super(ButtonGroup, self).height()
                    + self.padding + self.extra_padding[1]
                    + self.extra_padding[3])
        return self.define_rect[3]
