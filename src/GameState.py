__all__ = ["GameState"]

import pygame
import pygame.gfxdraw
from pygame.locals import *

import util
import sys
import math

from State import State
from Actor import Actor
from Player import Player
from Vector2 import Vector2
from WorldLoader import WorldLoader
from TerrainLayer import TerrainLayer
import config

IMG_HUD = "hud_bg.png"
IMG_HUD2 = "hud_bg2.png"
IMG_SLOT = "slot_bg.png"
IMG_HEART = "hud_health.png"
IMG_HEART2 = "hud_health_half.png"

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
		self.hud = Actor(IMG_HUD,-1)
		self.hud2 = Actor(IMG_HUD2)
		self.hud.setPos(32, config.HEIGHT/2)
		self.hud2.setPos(config.WIDTH - 32, config.HEIGHT/2)
		GameState.guiGroup.add(self.hud)
		GameState.guiGroup.add(self.hud2)
		self.health = 7
		self.hudHearts = []
		self.hudHeartsHalf = Actor(IMG_HEART2,-1)
		self.hudSlot = [None]*3
		self.wl = WorldLoader(config.WORLD_NAME)
		self.background = TerrainLayer("tygra/0_0.map")
		self.currentMap = "tygra/0_0.map"
		for i in range(0, 3):
			self.hudSlot[i] = Actor(IMG_SLOT, -1)
			self.hudSlot[i].setPos(50, 120 + i * 120)
			self.guiGroup.add(self.hudSlot[i])

		self.updateHudHealth()

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
		from config import keyboard
		super(GameState, self).update(clock);
		GameState.guiGroup.update(clock)
		GameState.playerGroup.update(clock, [x.rect for x in self.background.atGroup])

		# testing
		if keyboard.downup("HEALTHDOWN"):
			self.health -= 1
			self.updateHudHealth()
		if keyboard.downup("HEALTHUP"):
			self.health += 1
			self.updateHudHealth()

	def updateHudHealth(self):
		if self.health < 1 or self.health > 20:
			return

		full = self.health/2
		halve = self.health%2

		if len(self.hudHearts) != full:
			while len(self.hudHearts) < full:
				self.hudHearts.append(Actor(IMG_HEART,-1))
				GameState.guiGroup.add(self.hudHearts[-1])

			while len(self.hudHearts) > full:
				GameState.guiGroup.remove(self.hudHearts.pop())

			for i in range(0,full):
				self.hudHearts[i].setPos(config.WIDTH - 25, config.HEIGHT - 50 - i * 60)

		if halve == 1:
			GameState.guiGroup.add(self.hudHeartsHalf)
			self.hudHeartsHalf.setPos(config.WIDTH - 25, config.HEIGHT - 50 - full * 60)
		else:
			self.hudHeartsHalf.kill()

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

	# LEGACY CODE: Not called anymore, need to do something with health, hud stuff
	def handleKey(self, event):
		'''
			Handle input from user keyboard
		'''

		if event.type == pygame.KEYDOWN:
			# exit game
			if event.key == K_ESCAPE:
				sys.exit(1)
			if event.key in KEY2DIRECTION:
				self.player.move(KEY2DIRECTION[event.key])
			if event.key == MAGIC_ATTACK_KEY:
				self.player.useMagic()
			# testing
			if event.key == K_DOWN:
				self.health -= 1
				self.updateHudHealth()
			if event.key == K_UP:
				self.health += 1
				self.updateHudHealth()

		elif event.type == pygame.KEYUP:
			if event.key in KEY2DIRECTION:
				self.player.unMove(KEY2DIRECTION[event.key])

		elif event.type == pygame.MOUSEBUTTONDOWN:
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

	def draw(self):
		#draw background
		#self.main.screen.blit(self.background, self.background.get_rect())
		self.background.drawTerrain(self.main.screen);

		# draw player
		GameState.playerGroup.draw(self.main.screen)

		# draw gui
		GameState.guiGroup.draw(self.main.screen)

		# flip screen
		super(GameState, self).draw()

