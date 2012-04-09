from State import State
import pygame
import pygame.gfxdraw
import util
import sys
from Actor import Actor
from pygame.locals import *
from GameState import GameState
from config import WIDTH, HEIGHT

IMG_TITLE_SCREEN = "screen_title.png"
IMG_LABEL_START = "label_start.png"
IMG_LABEL_START2 = "label_start_flash.png"

class TitleState(State):
	titleGroup = pygame.sprite.GroupSingle()
	btnStartGroup = pygame.sprite.GroupSingle()
	
	def __init__(self, main):
		# transition from another state
		State.__init__(self,main)
		self.titleScreen = Actor(IMG_TITLE_SCREEN)
		self.btnStart = Actor(IMG_LABEL_START)
		self.btnStart2 = Actor(IMG_LABEL_START2)
		
		self.btnStart.setPos(WIDTH/2,HEIGHT-300)
		self.btnStart2.setPos(WIDTH/2,HEIGHT-300)
		
		self.tick = 0
		self.tickInterval = 60
		self.ready = False

		TitleState.titleGroup.add(self.titleScreen)
		TitleState.btnStartGroup.add(self.btnStart)
		
		pygame.mixer.init()
		pygame.mixer.music.load("../data/sounds/godspeed.mid")
		pygame.mixer.music.play()
		
	def __del__(self):
		# transition to another state
		TitleState.titleGroup.empty()
		TitleState.btnStartGroup.empty()
		pygame.mixer.music.stop()
		
	def update(self):
		self.tick += 1
		
		if self.tick < self.tickInterval/4: 
			TitleState.btnStartGroup.add(self.btnStart2)
		else:
			TitleState.btnStartGroup.add(self.btnStart)
			
		if self.tick > self.tickInterval:
			self.tick = 0
			if self.ready:
				self.main.changeState(GameState(self.main))
				
		
		TitleState.btnStartGroup.update()
		TitleState.titleGroup.update()
		State.update(self)
	
	def handleEvent(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
				if event.key == K_RETURN:
					pygame.mixer.music.stop()
					pygame.mixer.music.load("../data/sounds/HeroOh.mp3")
					pygame.mixer.music.play()				
					self.ready = True
					self.tick = 0
					self.tickInterval = 120
		
	def draw(self):
		# draw group stuff
		TitleState.titleGroup.draw(self.main.screen)
		TitleState.btnStartGroup.draw(self.main.screen)
		State.draw(self)
