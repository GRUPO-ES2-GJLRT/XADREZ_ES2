import pygame

from base import Scene


class MainMenu(Scene):

	def __init__(self):
		self.status = 0

	def draw(self, game, delta_time):
		game.screen.fill((self.status*50, 0, 0))

	def event(self, game, delta_time, event):
		if event.type == pygame.MOUSEBUTTONUP:
			self.status += 1
		if self.status*50 > 255:
			#self.status = 3
			game.scene = Scene()

