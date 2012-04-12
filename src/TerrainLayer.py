import pygame
import pygame.sprite
import util
import sys
import math
import Map

from config import *

class TerrainLayer(pygame.Surface):
	'''
		This builds a map background
	'''
	
	def __init__(self, mapname):
		#make a surface
		#load the images
		#blit onto that shit.
		#pygame.Surface.__init__((WIDTH, HEIGHT))
		super(TerrainLayer,self).__init__((WIDTH,HEIGHT))
		self.fill([0,0,0])
		
		thismap = Map.Map(mapname)
		
		imagekeys = thismap.aliases.keys()
		imagemap = {}
		for x in imagekeys:
			#load the image and key it the same
			temp,tmp = util.loadImage(thismap.aliases[x])
			temptile = pygame.Surface((TILEX,TILEY))
			temptile.blit(temp, tmp)
			imagemap[x] = temptile


		#blit the tiles...
		for y in range(HEIGHT/TILEY):
			for x in range(0, (WIDTH/TILEX)-4):
				if not thismap.belowLayer[y][x] == '.':
					self.blit(imagemap[thismap.belowLayer[y][x]], ((x+2)*TILEX, y*TILEY))

		#load sprites for at layer
		self.atGroup = pygame.sprite.RenderPlain()
		for y in range(HEIGHT/TILEY):
			for x in range(0, (WIDTH/TILEX)-4):
				if not thismap.atLayer[y][x] == '.':
					sprite = pygame.sprite.Sprite(self.atGroup)
					sprite.image, sprite.rect = util.loadImage(thismap.aliases[thismap.atLayer[y][x]])
					sprite.rect.topleft = ((x+2)*TILEX, y*TILEY)

	def drawTerrain(self,screen):
		screen.blit(self,self.get_rect())
		self.atGroup.draw(screen)
