__all__ = ["TitleState"]

from State import State
import pygame
import pygame.gfxdraw
import util
import sys
from Actor import Actor
from pygame.locals import *
from GameState import GameState
import config

IMG_TITLE_SCREEN = "screen_title.png"
IMG_LABEL_START = "label_start.png"
IMG_LABEL_START2 = "label_start_flash.png"

class TitleState(State):
	titleGroup = pygame.sprite.GroupSingle()
	btnStartGroup = pygame.sprite.GroupSingle()

	def __init__(self, main):
		# transition from another state
		super(TitleState, self).__init__(main)
		self.titleScreen = Actor(IMG_TITLE_SCREEN)
		self.btnStart = Actor(IMG_LABEL_START)
		self.btnStart2 = Actor(IMG_LABEL_START2)

		self.btnStart.setPos(config.WIDTH/2, config.HEIGHT - 300)
		self.btnStart2.setPos(config.WIDTH/2, config.HEIGHT - 300)

		self.tick = 0
		self.tickInterval = 60

		TitleState.titleGroup.add(self.titleScreen)
		TitleState.btnStartGroup.add(self.btnStart)

		'''TODO: FIX MUSIC
		pygame.mixer.init()
		pygame.mixer.music.load("../data/sounds/godspeed.mid")
		pygame.mixer.music.play()
		'''

	def __del__(self):
		# transition to another state
		TitleState.titleGroup.empty()
		TitleState.btnStartGroup.empty()
		'''TODO: FIX MUSIC
		pygame.mixer.music.stop()
		'''
		super(TitleState, self).__del__()

	def update(self, clock):
		super(TitleState, self).update(clock)
		self.tick += 1

		if self.tick < self.tickInterval/4:
			TitleState.btnStartGroup.add(self.btnStart2)
		else:
			TitleState.btnStartGroup.add(self.btnStart)

		if config.keyboard.downup("START"):
			self.main.changeState(GameState(self.main))

		TitleState.btnStartGroup.update(clock)
		TitleState.titleGroup.update(clock)

	def handleEvent(self):
		super(TitleState, self).handleEvent()
		'''TODO: FIX MUSIC
		pygame.mixer.music.stop()
		pygame.mixer.music.load("../data/sounds/HeroOh.ogg")
		pygame.mixer.music.play()
		'''

	def draw(self):
		# draw group stuff
		TitleState.titleGroup.draw(self.main.screen)
		TitleState.btnStartGroup.draw(self.main.screen)
		super(TitleState, self).draw()

