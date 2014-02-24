import time
import pygame

from scenes.main_menu import MainMenu as Scene


WIDTH, HEIGHT = 1024, 768


class Game(object):

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.running = True
        self.scene = Scene()


    def loop(self):
        '''Infinite loop for the game'''
        last_frame_time = 0

        while self.running:
            current_time = time.time()
            delta_time = current_time - last_frame_time
            last_frame_time = current_time

            self.scene.loop(self, delta_time)


def main():
    game = Game(WIDTH, HEIGHT)
    game.loop()

if __name__ == '__main__':
    main()