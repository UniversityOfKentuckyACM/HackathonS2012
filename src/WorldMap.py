
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

		# Don't display by default
		self.show = False

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

		# Make game a faded out to draw attentiont to map.
		# Fill it with black and add an alpha. Game should appear to "fade"
		self.fadeSurface = pygame.Surface((config.WIDTH, config.HEIGHT))
		self.fadeSurface.fill((0,0,0))
		self.fadeSurface.set_alpha(180)

	def genImage(self, row, col):
		# Load current map
		layer = TerrainLayer(self.wl.world[(col,row)])
		map = Map(self.wl.world[(col, row)])

		# Grab a dict of tilename -> image
		tiles = layer.imagemap

		# Store the avg color of each tile
		tileVals = {}

		# now determine the average color of each tile
		for tile, img in tiles.items():
			avgR = 0
			avgG = 0
			avgB = 0
			for x in range(0,config.TILEX,2):
				for y in range(0,config.TILEY,2):
					r,g,b,a = img.get_at((x,y))
					avgR += r
					avgG += g
					avgB += b

			avgR /= config.TILEX * config.TILEY / 4
			avgG /= config.TILEX * config.TILEY / 4
			avgB /= config.TILEX * config.TILEY / 4

			# Store average value
			# 255 = opaque
			tileVals[tile] = (avgR, avgG, avgB, 255)

		# Top left corner of where we'll draw
		startx = col * Map.NUM_COLS * WorldMap.PIXELS_PER_TILE
		starty = row * Map.NUM_ROWS * WorldMap.PIXELS_PER_TILE

		# for each tile in current map
		for i in range(Map.NUM_COLS):
			# x coordinate to draw
			x = startx + (i * WorldMap.PIXELS_PER_TILE)

			# Traverse row
			for j in range(Map.NUM_ROWS):
				# y coordinate to draw
				y = starty + (j * WorldMap.PIXELS_PER_TILE)

				# map is x,y so swap j and i
				tile = '.'
				if map.overLayer[j][i] != '.':
					tile = map.overLayer[j][i]
				elif map.atLayer[j][i] != '.':
					tile = map.atLayer[j][i]
				else:
					tile = map.belowLayer[j][i]

				# Draw each tile as a 2x2 block
				if tile != '.':
					self.surface.set_at((x,y), tileVals[tile])
					self.surface.set_at((x+1,y), tileVals[tile])
					self.surface.set_at((x,y+1), tileVals[tile])
					self.surface.set_at((x+1,y+1), tileVals[tile])

	def update(self, clock):
		from config import keyboard, keymap
		if keyboard.downup(keymap.MAP):
			self.show = not self.show

	def draw(self, screen):
		if self.show:
			screen.blit(self.fadeSurface, (0,0))
			screen.blit(self.surface, self.pos)

