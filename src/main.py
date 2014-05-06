import kivy
kivy.require('1.0.6')

from kivy.app import App
from game import Game

WIDTH, HEIGHT = 1024, 768


class ChessApp(App):
    title = 'Chess'

    def build(self):
        game = Game(WIDTH, HEIGHT)
    	game.loop()
	return True

    def on_pause(self):
        return True

if __name__ == '__main__':
    ChessApp().run()
