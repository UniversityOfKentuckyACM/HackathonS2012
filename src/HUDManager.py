# Prevents pygame.sprite.Sprite from being exported in the event of
# from HUDManager import *
__all__ = ["HUDManager"]

import pygame
from pygame.sprite import Sprite

import GameState

import config
import util

# HUD config
NUM_SLOTS = 3
SLOT_SPACING = 120
SLOT_INDENT_LEFT = 20
SLOT_INDENT_TOP = 200
HEART_SPACING = 70
HEART_INDENT_RIGHT = config.WIDTH
HEART_INDENT_BOTTOM = config.HEIGHT - 50

# Image names
IMG_LEFTBAR = "hud_bg.png"
IMG_RIGHTBAR = "hud_bg2.png"
IMG_SLOT = "slot_bg.png"
IMG_HEART = "hud_health.png"
IMG_HEARTHALF = "hud_health_half.png"

class HUDElement(Sprite):
	def __init__(self, imageFile=None, colorKey=None):
		super(HUDElement, self).__init__()

		if imageFile is not None:
			self.image, self.rect = util.loadImage(imageFile, colorKey)

	def placeLeft(self, x, y):
		self.rect.left = x
		self.rect.top = y

	def placeRight(self, x, y):
		self.rect.right = x
		self.rect.top = y


class HUDManager(object):
	def __init__(self):
		# Create sprite group for updating and drawing.
		self.elementGroup = pygame.sprite.OrderedUpdates()

		# Left bar of HUD -- eventually to be used for weapon slots, etc.
		# Placed along left side of screen
		self.leftBar = HUDElement(IMG_LEFTBAR)
		self.leftBar.placeLeft(0, 0)
		self.elementGroup.add(self.leftBar)

		# Place right bar of HUD along right side of screen
		self.rightBar = HUDElement(IMG_RIGHTBAR)
		self.rightBar.placeRight(config.WIDTH,0)
		self.elementGroup.add(self.rightBar)

		# Place NUM_SLOTS weapon slots on the left bar of HUD. These are
		# currently just decoration, but ideally will be show equipment, etc.
		self.slots = []
		for i in range(NUM_SLOTS):
			self.slots.append(HUDElement(IMG_SLOT))
			self.slots[i].placeLeft(
				SLOT_INDENT_LEFT,
				SLOT_INDENT_TOP + (SLOT_SPACING * i)
			)
			self.elementGroup.add(self.slots[i])

		# Initialize health 'hearts'.
		self.hearts = []

		self.updateHealth(10)

	def updateHealth(self, health):
		'''
			Accept health (integer) and the corresponding amount of health on
			rightBar. One health corresponds to half of a circle.

			We generate a new list of sprites each time we update health. Not
			the most efficient option, but there won't be enough hearts or
			enough update calls to create any performance issues. Shut up Chris.
		'''
		for i in self.hearts:
			i.kill()

		# Every heart = 2 health
		for i in range(health / 2):
			self.hearts.append(HUDElement(IMG_HEART))
			self.hearts[i].placeRight(
				HEART_INDENT_RIGHT,
				HEART_INDENT_BOTTOM - (HEART_SPACING * i)
			)
			self.elementGroup.add(self.hearts[i])

		# Add a half heart if necessary
		if health % 2 == 1:
			self.hearts.append(HUDElement(IMG_HEARTHALF))
			self.hearts[-1].placeRight(
				HEART_INDENT_RIGHT,
				HEART_INDENT_BOTTOM - (HEART_SPACING * (len(self.hearts) - 1))
			)
			self.elementGroup.add(self.hearts[-1])

	def update(self, clock, player):
		self.updateHealth(player.getHealth())

	def draw(self, screen):
		self.elementGroup.draw(screen)

