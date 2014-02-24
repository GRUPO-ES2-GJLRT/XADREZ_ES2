import time
import pygame

from scenes.main_menu import MainMenu as Scene


WIDTH, HEIGHT = 1024, 768

def relative(value, size):
    result = value * size
    return int(max(0, min(size - 1, result)))

class Game(object):

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.running = True
        self.scene = None
        
    def loop(self):
        '''Infinite loop for the game'''
        self.scene = Scene(self)
        last_frame_time = 0

        while self.running:
            current_time = time.time()
            delta_time = current_time - last_frame_time
            last_frame_time = current_time

            self.scene.loop(delta_time)

    def relative_x(self, x):
        '''Returns the coordinate X relative to the screen width
        Arguments:
        x: float [0..1]
        '''
        return relative(x, self.width)

    def relative_y(self, y):
        '''Returns the coordinate Y relative to the screen height
        Arguments:
        y: float [0..1]
        '''
        return relative(y, self.height)


def main():
    game = Game(WIDTH, HEIGHT)
    game.loop()

if __name__ == '__main__':
    main()