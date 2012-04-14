
import pygame

from Map import Map

import config

class WorldMap(object):

	def __init__(self, loader):
		# Grab WorldLoader
		self.wl = loader
		
		# Dimensions of worlds
		self.worldDimRows = self.wl.rows
		self.worldDimCols = self.wl.cols

		# Determine dimensions of image
		self.dimX = self.wl.cols * Map.NUM_COLS
		self.dimY = self.wl.rows * Map.NUM_ROWS

		self.surface = pygame.Surface((self.dimX, self.dimY))
		for i in range(self.dimX):
			for j in range(self.dimY):
				self.surface.set_at((i,j), (200, 10, 200, 0))

		# Iterate through each map and generate image
		for i in range(self.worldDimRows):
			for j in range(self.worldDimCols):
				pass
		
	def genImage(self, row, col):
		pass
	
	def draw(self, screen):
		screen.blit(self.surface, (300,300))
		
