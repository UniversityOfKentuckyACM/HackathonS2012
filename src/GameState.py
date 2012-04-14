__all__ = ["GameState"]

import pygame
import pygame.gfxdraw
from pygame.locals import *

import util
import sys
import math
import os

from State import State
from Actor import Actor
from Player import Player
from WorldLoader import WorldLoader
from WorldMap import WorldMap
from HUDManager import HUDManager
from Vector2 import Vector2
import config
class GameState(State):
	'''
		State for game playing mode.
	'''

	bgGroup = pygame.sprite.OrderedUpdates()
	playerGroup = pygame.sprite.RenderPlain()
	guiGroup = pygame.sprite.OrderedUpdates()

	def __init__(self, main):
		# transition from another state
		super(GameState, self).__init__(main)
		self.loadPlayer()

		# Initialize World
		self.wl = WorldLoader(config.WORLD_NAME)
		startMap = os.path.join("tygra", "0_0.map") 
		self.background = self.wl.getMap(startMap)
		self.currentMap = startMap
		
		# Initialize World Map
		self.worldMap = WorldMap(self.wl)
		
		# Initialize HUD
		self.hud = HUDManager()
		'''TODO: FIX MUSIC pygame.mixer.init() filename = "worldAmbient.ogg"
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
		self.player.mapPos = [0,0]
		GameState.playerGroup.add(self.player)

	def update(self, clock):
		super(GameState, self).update(clock);
		GameState.guiGroup.update(clock)
		GameState.playerGroup.update(clock, [x.rect for x in self.background.atGroup])

		self.worldMap.update(clock)

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
			# update player mapPos
			self.player.mapPos[1] -= 1
			# position player at bottom minus almost half a tile
			if mmap is not None:
				self.player.setPos(pos[0], config.HEIGHT - 17)
		elif direction == 'down':
			mmap = self.wl.south[self.currentMap]
			self.player.mapPos[1] += 1
			if mmap is not None:
				self.player.setPos(pos[0], 17)
		elif direction == 'right':
			self.player.mapPos[0] += 1
			mmap = self.wl.east[self.currentMap]
			if mmap is not None:
				self.player.setPos(64 + 17, pos[1]) # just not touching the hud
		elif direction == 'left':
			self.player.mapPos[0] -= 1
			mmap = self.wl.west[self.currentMap]
			if mmap is not None:
				self.player.setPos(config.WIDTH - (64 + 17), pos[1])

		if mmap is not None:
			self.currentMap = mmap
			self.background = self.wl.getMap(mmap)

      		# Added for debugging purposes. Remove when not needed
        	print "MAP: ", mmap

	def draw(self):
		#draw background
		self.background.drawTerrain(self.main.screen);

		# draw player
		GameState.playerGroup.draw(self.main.screen)

		# draw gui
		self.hud.draw(self.main.screen)

		# draw world map
		self.worldMap.draw(self.main.screen)

		# flip screen
		super(GameState, self).draw()

