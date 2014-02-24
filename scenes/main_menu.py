import pygame

from base import Scene


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super(MainMenu, self).__init__(*args, **kwargs)
		self.status = 0

	def draw(self, delta_time):
		self.game.screen.fill((self.status*50, 0, 0))

	def event(self, delta_time, event):
		if event.type == pygame.MOUSEBUTTONUP:
			self.status += 1
		if self.status*50 > 255:
			#self.status = 3
			self.game.scene = Scene(self.game)

