__all__ = ["State"]

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP
from config import keyboard

class State(object):
	def __init__(self, main):
		# transition from another state
		self.main = main

	def __del__(self):
		# transition to another state
		pass

	def update(self, clock):
		# update
		self.handleEvent()
		self.draw()

	def handleEvent(self):
		# handle events
		for event in pygame.event.get((KEYDOWN, KEYUP)):
			keyboard.handle(event)
		for event in pygame.event.get(QUIT):
			sys.exit(0)

	def draw(self):
		# draw group stuff
		pygame.display.flip()

