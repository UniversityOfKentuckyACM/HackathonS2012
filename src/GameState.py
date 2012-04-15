__all__ = ["GameState"]

import pygame
import pygame.gfxdraw
from pygame.locals import *

import util
import sys
import math
import os

import NPC
from Enemy import Enemy

from random import *

from State import State
from Actor import Actor
from Player import Player
from WorldLoader import WorldLoader
from TerrainLayer import TerrainLayer
from HUDManager import HUDManager
from Vector2 import Vector2
from time import *
import config

class GameState(State):
	'''
		State for game playing mode.
	'''
	bgGroup = pygame.sprite.OrderedUpdates()
	playerGroup = pygame.sprite.RenderPlain()
	guiGroup = pygame.sprite.OrderedUpdates()
	enemyGroup = pygame.sprite.RenderPlain()
	player = None
	terrainLayer = None
	cachedPathGraph = None
	curPathGraph = None

	def getPlayer():
		assert(player != None)
		return GameState.player
	
	@staticmethod
	def getCurrentAtMap():
		assert(GameState.terrainLayer != None)
		return GameState.terrainLayer.getMap().getAtLayer()

	def __init__(self, main):
		# transition from another state
		super(GameState, self).__init__(main)
		self.loadPlayer()
        
		self.wl = WorldLoader(config.WORLD_NAME)
		startMap = os.path.join("tygra", "0_0.map") 
		self.background = TerrainLayer(startMap)
		GameState.terrainLayer = self.background
		self.currentMap = startMap
		self.hud = HUDManager()
		self.timesincelastdamage = 0
		
		GameState.enemyGroup.add(Enemy(self, self.player.rect.left, self.player.rect.top, "skeleton"))
		GameState.enemyGroup.sprites()[0].movetowards(self.player.rect.left, self.player.rect.top)

		''' npc_one = NPC(self, 30, 30, "Skeleton") '''
		'''TODO: FIX MUSIC
		pygame.mixer.init()
		filename = "worldAmbient.ogg"
		path = os.path.join(util.GAME_SOUNDS, filename)
		path = util.filepath(path)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play()
		'''

	def __del__(self):
		# transition to another state
		super(GameState, self).__del__()

	def loadPlayer(self):
		self.player = Player(self)
		GameState.player = self.player
		GameState.playerGroup.add(self.player)

	def update(self, clock):
		super(GameState, self).update(clock)
		GameState.guiGroup.update(clock)
		GameState.playerGroup.update(clock, [x.rect for x in self.background.atGroup])
		for i in range(0, len(GameState.enemyGroup.sprites())):
			x = (self.player.rect.left + self.player.rect.right) / 2
			y = (self.player.rect.top + self.player.rect.bottom) / 2
			GameState.enemyGroup.sprites()[i].movetowards(x, y)

			if (self.player.rect.colliderect(GameState.enemyGroup.sprites()[i].rect)):
				GameState.enemyGroup.sprites()[i].attack(self.player, 1)
				print "AAAAAHHHHHHHHH!!!!!"

		GameState.enemyGroup.update(clock, [x.rect for x in self.background.atGroup])
		self.hud.update(clock, self.player)

	def handleEvent(self):
		super(GameState, self).handleEvent()

		# handle mouse
		mousePos = Vector2(pygame.mouse.get_pos())
		self.player.orient(mousePos)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					self.player.swingSword()
				if pygame.mouse.get_pressed()[2]:
					self.player.shootBow()

	def nextMap(self, direction, pos):
		# print "moving to: " + direction + " via: " + str(pos)
		mmap = None

		if direction == 'up':
			mmap = self.wl.north[self.currentMap]
			# position player at bottom minus almost half a tile
			if mmap is not None:
				self.player.setPos(pos[0], config.HEIGHT - 17)
		elif direction == 'down':
			mmap = self.wl.south[self.currentMap]
			if mmap is not None:
				self.player.setPos(pos[0], 17)
		elif direction == 'right':
			mmap = self.wl.east[self.currentMap]
			if mmap is not None:
				self.player.setPos(64 + 17, pos[1]) # just not touching the hud
		elif direction == 'left':
			mmap = self.wl.west[self.currentMap]
			if mmap is not None:
				self.player.setPos(config.WIDTH - (64 + 17), pos[1])

		if mmap is not None:
			self.currentMap = mmap
			self.background = TerrainLayer(mmap)

      		# Added for debugging purposes. Remove when not needed
        	print "MAP: ", mmap
		GameState.enemyGroup.empty()
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))

	def draw(self):
		#draw background
		#self.main.screen.blit(self.background, self.background.get_rect())
		self.background.drawTerrain(self.main.screen);

		# draw player
		GameState.playerGroup.draw(self.main.screen)
		
		GameState.enemyGroup.draw(self.main.screen)

		# draw gui
		self.hud.draw(self.main.screen)

		# flip screen
		super(GameState, self).draw()

