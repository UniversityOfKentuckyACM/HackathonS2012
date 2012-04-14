__all__ = ["Player"]

import math
import pygame.sprite
import Collider
import util

from Vector2 import Vector2
from Magic import Magic

import config

# Player idle sprites
PLAYER_IDLE_UP = "characterUp1.png"
PLAYER_IDLE_DOWN = "characterDown1.png"
PLAYER_IDLE_LEFT = "characterLeft1.png"
PLAYER_IDLE_RIGHT = "characterRight1.png"

# Sword sprites
SWORD_UP = "swordSwingUp.png"
SWORD_DOWN = "swordSwingDown.png"
SWORD_LEFT = "swordSwingLeft.png"
SWORD_RIGHT = "swordSwingRight.png"

# Direction enum
UP, DOWN, LEFT, RIGHT = range(4)

# Staring position
START_X = config.WIDTH / 2
START_Y = config.HEIGHT / 2

# Speed
PLAYER_SPEED = 8

class Player(Collider.Collider):
	'''
		Player class. images is a list of images for each direction. We may need
		to alter this to support animation.
	'''

	def __init__(self,gameState):
		super(Player,self).__init__()

		# load all images
		# up, down, left, right
		self.images = [0] * 4
		self.images[UP],    self.rect = util.loadImage(PLAYER_IDLE_UP)
		self.images[DOWN],  self.rect = util.loadImage(PLAYER_IDLE_DOWN)
		self.images[LEFT],  self.rect = util.loadImage(PLAYER_IDLE_LEFT)
		self.images[RIGHT], self.rect = util.loadImage(PLAYER_IDLE_RIGHT)

		self.direction = UP

		# assign image and position
		self.setImage(self.images[self.direction])
		self.setPos(START_X, START_Y)

		# load sword
		self.swordLeft = pygame.sprite.Sprite()
		self.swordLeft.image, self.swordLeft.rect  = util.loadImage(SWORD_LEFT)
		self.swordUp = pygame.sprite.Sprite()
		self.swordUp.image, self.swordUp.rect = util.loadImage(SWORD_UP)
		self.swordRight = pygame.sprite.Sprite()
		self.swordRight.image, self.swordRight.rect = util.loadImage(SWORD_RIGHT)
		self.swordDown = pygame.sprite.Sprite()
		self.swordDown.image, self.swordDown.rect = util.loadImage(SWORD_DOWN)

		self.gameState = gameState

		#health
		self.health = 10
		self.alive = True

	# Orient player with mouse
	def orient(self, mousePos):
		loc = mousePos - Vector2(self.getPos())
		angle = math.atan2(loc.x, loc.y)
		mag = math.fabs(angle)

		# if we're facing to the right
		if mag < math.pi / 4:
			self.setDir(DOWN)
		# move left
		elif mag > 3 * math.pi / 4:
			self.setDir(UP)
		# either up or down
		else:
			if angle < 0:
				self.setDir(LEFT)
			else:
				self.setDir(RIGHT)

	def setDir(self, newDir):
		self.direction = newDir
		self.image = self.images[self.direction]

	# TODO: FIX THIS
	def swingSword(self):
		'''
			When left mouse is pressed, sword is pushed out
		'''

		if self.direction == UP:
			self.swordUp.rect.bottomleft = self.rect.topleft
			self.swordUp.add(self.gameState.playerGroup)
		elif self.direction == DOWN:
			self.swordDown.rect.topleft = self.rect.bottomleft
			self.swordDown.add(self.gameState.playerGroup)
		elif self.direction == LEFT:
			self.swordLeft.rect.topright = self.rect.topleft
			self.swordLeft.add(self.gameState.playerGroup)
		elif self.direction == RIGHT:
			self.swordRight.rect.topleft = self.rect.topright
			self.swordRight.add(self.gameState.playerGroup)

	# TODO: Add to this
	def shootBow(self):
		'''
		When right mouse is pressed, arrow is fire infront of character
	'''
		print "Arrow Fired"

	# TODO: Add to this
	def useMagic(self):
			'''
			When space bar is pressed, magic is thrown towards the mouse pointer
			Or infront of the character *Choice*
			'''
			pos = self.rect.center
			self.magi = Magic(pos[0], pos[1])

			self.magi.add(self.gameState.playerGroup)

	def update(self, clock, environment):
		from config import keyboard, keymap

		#am i alive?
		if (self.health <= 0):
			self.alive = False

		vel = Vector2(0, 0);
		if keyboard.down(keymap.UP):
			vel.y -= 1
		elif keyboard.down(keymap.DOWN):
			vel.y += 1
		if keyboard.down(keymap.LEFT):
			vel.x -= 1
		elif keyboard.down(keymap.RIGHT):
			vel.x += 1
		self.vel = vel.normalized() * PLAYER_SPEED

		super(Player, self).update(clock, environment, False)

		if keyboard.downup(keymap.MAGIC):
			self.useMagic()

		# Check to see if we have touched edge of the screen
		if self.rect.left < config.TILEX * 2:
			self.gameState.nextMap("left", self.getPos())
		elif self.rect.right > config.WIDTH - config.TILEX * 2:
			self.gameState.nextMap("right", self.getPos())
		elif self.rect.top < 0:
			self.gameState.nextMap("up", self.getPos())
		elif self.rect.bottom > config.HEIGHT:
			self.gameState.nextMap("down", self.getPos())

	def getHealth(self):
		return self.health

	def damaged(self, damage):
		self.health -= damage

	def attack(self, target, damage):
		target.damaged(damage)

