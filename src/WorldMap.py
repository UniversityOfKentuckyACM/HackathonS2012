
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

		# Iterate through each map and generate image
		for i in range(self.worldDimRows):
			for j in range(self.worldDimCols):
				self.genImage(i,j)
		
	def genImage(self, row, col):
		print("(%d, %d)" % (row, col))
		# Load current map
		layer = TerrainLayer(self.wl.world[(row,col)])
		map = Map(self.wl.world[(row,col)])

		# Grab a dict of tilename -> image
		tiles = layer.imagemap
		
		# Store the avg color of each tile
		tileVals = {}

		# now determine the average color of each tile
		for tile, img in tiles.items():
			avgR = 0
			avgG = 0
			avgB = 0
			for x in range(config.TILEX):
				for y in range(config.TILEY):
					r,g,b,a = img.get_at((x,y))
					avgR += r
					avgG += g
					avgB += b

			avgR /= config.TILEX * config.TILEY
			avgG /= config.TILEX * config.TILEY
			avgB /= config.TILEX * config.TILEY

			# Store average value
			# 255 = opaque
			tileVals[tile] = (avgR, avgG, avgB, 255)
		
		# Top left corner of where we'll draw
		startx = col * Map.NUM_COLS * WorldMap.PIXELS_PER_TILE
		starty = row * Map.NUM_ROWS * WorldMap.PIXELS_PER_TILE

		# for each tile in current map
		for i in range(Map.NUM_ROWS):
			# y coordinate to draw
			y = starty + (i * WorldMap.PIXELS_PER_TILE)
			
			# Traverse row
			for j in range(Map.NUM_COLS):
				# x coordinate to draw
				x = startx + (j * WorldMap.PIXELS_PER_TILE)

				tile = '.'
				if map.atLayer[i][j] != '.':
					tile = map.atLayer[i][j]
				else:
					tile = map.belowLayer[i][j]

				if tile != '.':
					self.surface.set_at((x,y), tileVals[tile])
					self.surface.set_at((x+1,y), tileVals[tile])
					self.surface.set_at((x,y+1), tileVals[tile])
					self.surface.set_at((x+1,y+1), tileVals[tile])
					'''
					for currX in range(WorldMap.PIXELS_PER_TILE):
						for currY in range(WorldMap.PIXELS_PER_TILE):
							self.surface.set_at((startx+currX, starty+currY), tileVals[tile])
					'''


	def draw(self, screen):
		screen.blit(self.surface, self.pos)
		
