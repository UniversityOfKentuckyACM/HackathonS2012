
import pygame

from Map import Map
from TerrainLayer import TerrainLayer

import config

class WorldMap(object):
	
	# How many pixels (in each dimension) we use to represent each tile
	PIXELS_PER_TILE = 2

	def __init__(self, loader):
		# Grab WorldLoader
		self.wl = loader
		
		# Dimensions of worlds
		self.worldDimRows = self.wl.rows
		self.worldDimCols = self.wl.cols

		# Determine dimensions of image
		self.dimX = self.wl.cols * Map.NUM_COLS * WorldMap.PIXELS_PER_TILE
		self.dimY = self.wl.rows * Map.NUM_ROWS * WorldMap.PIXELS_PER_TILE

		# Positioned by top-left corner -- center it
		self.pos = ((config.WIDTH / 2) - (self.dimX / 2), 
			(config.HEIGHT / 2) - (self.dimY / 2))

		# Create surface to draw on
		self.surface = pygame.Surface((self.dimX, self.dimY))

		# TEMP
		for i in range(self.dimX):
			for j in range(self.dimY):
				self.surface.set_at((i,j), (200, 10, 200, 0))

		# Iterate through each map and generate image
		for i in range(self.worldDimRows):
			for j in range(self.worldDimCols):
				self.genImage(i,j)
		
	def genImage(self, row, col):
		# Load current map
		layer = TerrainLayer(self.wl.world[(row,col)])

		# Grab a list of tiles in current map
		tiles = layer.imagemap

	def draw(self, screen):
		screen.blit(self.surface, self.pos)
		
