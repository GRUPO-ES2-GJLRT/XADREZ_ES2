import pygame


class Scene(object):

    def __init__(self, game):
        """ Scene constructor 

        Arguments:
        game is a Game instance
        """
        self.game = game

    def loop(self, delta_time):
        '''This function is called in the game loop. 

        Arguments:
        delta_time is the time in seconds (float) passed since 
            the last execution

        It calls the method self.event for each event and calls the method
            self.draw once to draw the screen
        '''
        self.game.screen.fill((0, 0, 0))

        self.draw(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            else:
                self.event(delta_time, event)

        pygame.display.flip()

    def draw(self, delta_time):
        '''This function should draw the scene. 
        Override it in a subclass!

        Arguments:
        delta_time is the time in seconds (float) passed since 
            the last game loop execution
        '''
        pass

    def event(self, delta_time, event):
        '''This function should process the events. 
        Override it in a subclass!

        Arguments:
        game is a Game instance
        delta_time is the time in seconds (float) passed since 
            the last game loop execution
        event is the received event
        '''
        pass