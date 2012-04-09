#!/usr/bin/python

# Python includes
import sys

# Pygame includes
import pygame
from pygame.locals import *

# Game includes
from Vector2 import Vector2
from config import *
from GameState import GameState
from TitleState import TitleState

class Game():
	def __init__(self):
		# load background image
		#self.g.loadBackground(BACKGROUND_IMAGE)

		# Initialize our player and set its position to (50,50)
	#	self.player = self.g.loadPlayer(PLAYER_IMAGE)
		#self.player.setPos(START_X, START_Y)

		if IS_FULLSCREEN:
			self.screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN|DOUBLEBUF)
		else:
			self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		
		pygame.display.set_caption(GAME_TITLE)

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
			self.clock.tick(FRAME_RATE)

			# State machine
			if self.nextState != None:
				self.state = self.nextState
				self.nextState = None
			else:
				self.state.update()

if __name__ == '__main__':
	g = Game()
