__all__ = ["TerrainLayer"]

import pygame
import pygame.sprite
import util
import sys
import math
import Map

import config

class TerrainLayer(pygame.Surface):
	'''
		This builds a map background
	'''

	def __init__(self, mapname):
		#make a surface
		#load the images
		#blit onto that shit.
		#pygame.Surface.__init__((WIDTH, HEIGHT))
		super(TerrainLayer, self).__init__((config.WIDTH, config.HEIGHT))
		self.fill([0, 0, 0])

		thismap = Map.Map(mapname)

		imagekeys = thismap.aliases.keys()
		imagemap = {}
		for x in imagekeys:
			#load the image and key it the same
			image, rect = util.loadImage(thismap.aliases[x])
			surface = pygame.Surface((config.TILEX, config.TILEY))
			surface.blit(image, rect)
			imagemap[x] = surface


		#blit the tiles...
		for y in range(config.HEIGHT / config.TILEY):
			for x in range(config.WIDTH / config.TILEX - 4):
				if thismap.belowLayer[y][x] != '.':
					self.blit(imagemap[thismap.belowLayer[y][x]], ((x + 2) * config.TILEX, y * config.TILEY))

		#load sprites for at layer and over layer
		self.atGroup = pygame.sprite.RenderPlain()
		self.overGroup = pygame.sprite.RenderPlain()
		for y in range(config.HEIGHT / config.TILEY):
			for x in range(config.WIDTH / config.TILEX - 4):
				if thismap.atLayer[y][x] != '.':
					sprite = pygame.sprite.Sprite(self.atGroup)
					sprite.image, sprite.rect = util.loadImage(thismap.aliases[thismap.atLayer[y][x]])
					sprite.rect.topleft = ((x + 2) * config.TILEX, y * config.TILEY)
				if thismap.overLayer[y][x] != '.':
					sprite = pygame.sprite.Sprite(self.overGroup)
					sprite.image, sprite.rect = util.loadImage(thismap.aliases[thismap.overLayer[y][x]])
					sprite.rect.topleft = ((x + 2) * config.TILEX, y * config.TILEY)

	def drawBackground(self, screen):
		screen.blit(self, self.get_rect())
		self.atGroup.draw(screen)

	def drawForeground(self, screen):
		self.overGroup.draw(screen)

