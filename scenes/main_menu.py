import pygame

from base import Scene, GameText
from i18n import TITLE, ONE_PLAYER, TWO_PLAYERS, QUIT


class MainMenu(Scene):

    def __init__(self, *args, **kwargs):
        """MainMenu constructor. Creates texts and buttons"""
        super(MainMenu, self).__init__(*args, **kwargs)

        # Title
        title_font = pygame.font.SysFont("", self.game.relative_x(0.1))
        title = GameText(title_font, TITLE, True, (192, 192, 192))
        title.rect = self.center_rect(
            title.surface, 
            self.game.relative_y(0.2)
        )
        
        menu_font = pygame.font.SysFont("", self.game.relative_x(0.05))
        
        # One Player Button
        one_player = GameText(menu_font, ONE_PLAYER, True, (128, 128, 128))
        one_player.rect = self.center_rect(
            one_player.surface, 
            self.game.relative_y(0.45)
        )

        def one_player_click(game):
            game.scene = Scene(game) #TODO: Change to One Player Scene or Configure Scene

        one_player.click = one_player_click

        # Two Players Button
        two_players = GameText(menu_font, TWO_PLAYERS, True, (128, 128, 128))
        two_players.rect = self.center_rect(
            two_players.surface, 
            one_player.rect.bottom + self.game.relative_x(0.04)
        )

        def two_players_click(game):
            game.scene = Scene(game) #TODO: Change to Two Players Scene or Configure Scene

        two_players.click = two_players_click

        # Quit Button
        quit = GameText(menu_font, QUIT, True, (128, 128, 128))
        quit.rect = self.center_rect(
            quit.surface, 
            two_players.rect.bottom + self.game.relative_x(0.04)
        )

        def quit_click(game):
            game.running = False

        quit.click = quit_click


        self.texts = [title, one_player, two_players, quit]
        self.buttons = [one_player, two_players, quit]
    
    def draw(self, delta_time):
        """Draws MainMenu"""
        for text in self.texts:
            text.blit(self.game.screen)

    def event(self, delta_time, event):
        """Checks for mouse hover and mouse click"""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.color = (192, 192, 192)
                else:
                    button.color = (128, 128, 128)
                button.redraw()
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click(self.game)
        

