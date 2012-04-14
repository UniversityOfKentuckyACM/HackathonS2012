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
from TerrainLayer import TerrainLayer
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
		self.wl = WorldLoader(config.WORLD_NAME)
		startMap = os.path.join("tygra", "0_0.map")
		self.environment = TerrainLayer(startMap)
		self.currentMap = startMap

		self.hud = HUDManager()

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
		GameState.playerGroup.add(self.player)

	def update(self, clock):
		super(GameState, self).update(clock);
		GameState.guiGroup.update(clock)
		GameState.playerGroup.update(clock, [x.rect for x in self.environment.atGroup])

	def handleEvent(self):
		super(GameState, self).handleEvent()
		self.sudoNext()
		# handle mouse
		mousePos = Vector2(pygame.mouse.get_pos())
		self.player.orient(mousePos)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					self.player.swingSword()
				if pygame.mouse.get_pressed()[2]:
					self.player.shootBow()

	def sudoNext(self):
	#Used for debugging,
		from config import keyboard, keymap
		mmap = None
		if keyboard.downup(keymap.DUP):
			mmap = self.wl.north[self.currentMap]
		elif keyboard.downup(keymap.DDOWN):
			mmap = self.wl.south[self.currentMap]
		elif keyboard.downup(keymap.DLEFT):
			mmap = self.wl.west[self.currentMap]
		elif keyboard.downup(keymap.DRIGHT):
			mmap = self.wl.east[self.currentMap]
		if mmap is not None:
			self.currentMap = mmap
			self.environment = TerrainLayer(mmap)
			print "MAP: ", mmap


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
			self.environment = TerrainLayer(mmap)

      		# Added for debugging purposes. Remove when not needed
        	print "MAP: ", mmap

	def draw(self):
		#draw environment
		#self.main.screen.blit(self.environment, self.environment.get_rect())
		self.environment.drawBackground(self.main.screen);

		# draw player
		GameState.playerGroup.draw(self.main.screen)

		# draw gui
	#	self.hud.draw(self.main.screen)

		# draw foreground
		self.environment.drawForeground(self.main.screen)
		# flip screen
		super(GameState, self).draw()

