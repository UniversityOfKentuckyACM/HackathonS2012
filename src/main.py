#!/usr/bin/python

# Python includes
import sys

# Pygame includes
import pygame
from pygame.locals import *

# Game includes
from Vector2 import Vector2
from GameState import GameState
from TitleState import TitleState
import config

class Game(object):
	def __init__(self):
		# load background image
		#self.g.loadBackground(BACKGROUND_IMAGE)

		# Initialize our player and set its position to (50,50)
		#	self.player = self.g.loadPlayer(PLAYER_IMAGE)
		#self.player.setPos(START_X, START_Y)

		if config.IS_FULLSCREEN:
			self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), FULLSCREEN|DOUBLEBUF)
		else:
			self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

		pygame.display.set_caption("Tygra")

		# game clock
		self.clock = pygame.time.Clock()

		# game state
		self.state = TitleState(self)
		self.nextState = None

		# Loop until exit
		self.gameLoop()

	def changeState(self,state):
		self.nextState = state

	def gameLoop(self):

		while True:
			# ensure we're running at a stable FPS
			self.clock.tick(config.FRAME_RATE)

			# State machine
			if self.nextState != None:
				self.state = self.nextState
				self.nextState = None
			else:
				self.state.update(self.clock)

if __name__ == '__main__':
	g = Game()

