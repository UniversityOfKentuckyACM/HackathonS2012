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
from WorldMap import WorldMap
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

		# Initialize World
		self.wl = WorldLoader(config.WORLD_NAME)

		# Initialize World Map
		self.worldMap = WorldMap(self.wl)
		startMap = os.path.join("tygra", "0_0.map")

		# Starting map
		self.environment = self.wl.getMap(startMap, self.worldMap)
		self.currentMap = startMap


		# Initialize HUD
		self.hud = HUDManager()
		#TODO: FIX MUSIC pygame.mixer.init() filename = "worldAmbient.ogg"

		GameState.enemyGroup.add(Enemy(self, self.player.rect.left - 50, self.player.rect.top - 50, "skeleton"))
		GameState.enemyGroup.sprites()[0].movetowards(self.player.rect.left, self.player.rect.top)

		#''' npc_one = NPC(self, 30, 30, "Skeleton") '''
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
		self.player.mapPos = [0,0]

		GameState.playerGroup.add(self.player)

	def update(self, clock):
		super(GameState, self).update(clock)
		GameState.guiGroup.update(clock)

		enemies = [enemy for enemy in GameState.enemyGroup]
		surfaces = [surface for surface in self.environment.atGroup]

		GameState.playerGroup.update(clock, self.player, enemies, surfaces)
		GameState.enemyGroup.update(clock, self.player, enemies, surfaces)

		self.worldMap.update(clock)

		self.hud.update(clock, self.player)

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
			print "MAP: ", mmap
			self.environment = self.wl.getMap(mmap, self.worldMap)

			# Added for debugging purposes. Remove when not needed
			print "MAP: ", mmap

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
			self.environment = self.wl.getMap(mmap, self.worldMap)

      		# Added for debugging purposes. Remove when not needed
        	print "MAP: ", mmap
		GameState.enemyGroup.empty()
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))
		GameState.enemyGroup.add(Enemy(self, randrange(1, config.WIDTH), randrange(1, config.HEIGHT), "skeleton"))

	def draw(self):
		#draw environment
		self.environment.drawBackground(self.main.screen);

		# draw player
		GameState.playerGroup.draw(self.main.screen)

		# draw enemies
		GameState.enemyGroup.draw(self.main.screen)

		# draw gui
		self.hud.draw(self.main.screen)

		# draw foreground
		self.environment.drawForeground(self.main.screen)

		# draw world map
		self.worldMap.draw(self.main.screen)

		# flip screen
		super(GameState, self).draw()

