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
from config import *

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
		State.__init__(self,main)
		self.loadPlayer()
		self.hud = Actor(IMG_HUD,-1)
		self.hud2 = Actor(IMG_HUD2)
		self.hud.setPos(32,HEIGHT/2)
		self.hud2.setPos(WIDTH-32,HEIGHT/2)
		GameState.guiGroup.add(self.hud)
		GameState.guiGroup.add(self.hud2)
		self.health = 7
		self.hudHearts = []
		self.hudHeartsHalf = Actor(IMG_HEART2,-1)
		self.hudSlot = [None]*3
		self.wl = WorldLoader('new.world')	
		self.background = TerrainLayer("0_0.map")
		self.currentMap = "0_0.map"
		for i in range(0,3):
			self.hudSlot[i] = Actor(IMG_SLOT,-1)
			self.hudSlot[i].setPos(50,120+i*120)
			self.guiGroup.add(self.hudSlot[i])
			
		self.updateHudHealth()

		pygame.mixer.init()
		filename = "worldAmbient.mp3"
		path = os.path.join(util.GAME_SOUNDS, filename)
		path = util.filepath(path)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play()

	def __del__(self):
		# transition to another state
		pass
		
	def loadPlayer(self):
		self.player = Player(self)
		GameState.playerGroup.add(self.player)
	
	def update(self):
		self.checkCollisions()
		State.update(self);
		
		GameState.guiGroup.update()
		GameState.playerGroup.update()
		
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
				self.hudHearts[i].setPos(WIDTH-25,HEIGHT-50-i*60)
				
		if halve == 1:
			GameState.guiGroup.add(self.hudHeartsHalf)
			self.hudHeartsHalf.setPos(WIDTH-25, HEIGHT-50-full*60)
		else:
			self.hudHeartsHalf.kill()
	
	def handleEvent(self):
		# handle mouse
		mousePos = Vector2(pygame.mouse.get_pos())
		self.player.orient(mousePos)
			
		# For each event that occurs this frame
		for event in pygame.event.get():
			# If user exits the window
			if event.type == QUIT:
				sys.exit(0)

			# monitor keyboard
			self.handleKey(event)
		
	def handleKey(self, event):
		'''
			Handle input from user keyboard
		'''
		if event.type == pygame.KEYDOWN:
			# exit game
			if event.key == K_ESCAPE:
				sys.exit(1)
			if event.key == MOVEMENT_KEYS[0]:
				self.player.move(0)
			if event.key == MOVEMENT_KEYS[1]:
				self.player.move(1)
			if event.key == MOVEMENT_KEYS[2]:
				self.player.move(2)
			if event.key == MOVEMENT_KEYS[3]:
				self.player.move(3)
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
			if event.key == MOVEMENT_KEYS[0]:
				self.player.unMove(0)
			if event.key == MOVEMENT_KEYS[1]:
				self.player.unMove(1)
			if event.key == MOVEMENT_KEYS[2]:
				self.player.unMove(2)
			if event.key == MOVEMENT_KEYS[3]:
				self.player.unMove(3)

		elif event.type == pygame.MOUSEBUTTONDOWN:
            		if pygame.mouse.get_pressed()[0]:
                		self.player.swingSword()
            		if pygame.mouse.get_pressed()[2]:
                		self.player.shootBow()
			
	def checkCollisions(self):
		# Check for atLayer collisions 
		for hit in pygame.sprite.spritecollide(self.player, self.background.atGroup, 0):
			self.player.collideWall(hit)

	def nextMap(self, direction, pos):
		# print "moving to: " + direction + " via: " + str(pos)
		mmap = ""

		if direction == 'up':
			mmap = self.wl.north[self.currentMap]
			# position player at bottom minus almost half a tile
			if mmap is not 'none':
				self.player.setPos(pos[0], HEIGHT-17)
		elif direction == 'down':
			mmap = self.wl.south[self.currentMap]
			if mmap is not 'none':
				self.player.setPos(pos[0], 17)
		elif direction == 'right':
			mmap = self.wl.east[self.currentMap]
			if mmap is not 'none':
				self.player.setPos(64+17, pos[1]) # just not touching the hud
		elif direction == 'left':
			mmap = self.wl.west[self.currentMap]
			if mmap is not 'none':
				self.player.setPos(WIDTH-(64+17), pos[1])
		if not mmap == 'none':
			self.currentMap = mmap
			self.background = TerrainLayer(mmap)

      		# Added for debugging purposes. Remove when not needed
        	print "MAP: ",mmap
		
	def draw(self):
		#draw background
		#self.main.screen.blit(self.background, self.background.get_rect())
		self.background.drawTerrain(self.main.screen);	

		# draw player	
		GameState.playerGroup.draw(self.main.screen)
		
		# draw gui
		GameState.guiGroup.draw(self.main.screen)
		
		# flip screen
		State.draw(self)
