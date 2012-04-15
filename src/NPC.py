__all__ = ["NPC"]

import math
import pygame.sprite
import Collider
import util

from Vector2 import Vector2

import config

UP, DOWN, LEFT, RIGHT = range(4)
NPC_SPEED = 2
NPC_SPEED = 2

class NPC(Collider.Collider):
	STATE_STOPPED = 0
	STATE_MOVING = 1
	def __init__(self, gameState, x, y, npcname):
		#load all images
		super(NPC, self).__init__()
		self.images = [0] * 4
		self.images[UP], self.rect = util.loadImage(npcname + "Up.png")
		self.images[DOWN], self.rect = util.loadImage(npcname + "Down.png")
		self.images[LEFT], self.rect = util.loadImage(npcname + "Left.png")
		self.images[RIGHT], self.rect = util.loadImage(npcname + "Right.png")
		self.direction = UP
		self.setImage(self.images[self.direction])
		self.setPos(x, y)
		self.gameState = gameState
		self.state = NPC.STATE_STOPPED
		self.destination = None

	def hitplayer(self, clock, player):
		if self.collidex or self.collidey:
			self.state = NPC.STATE_STOPPED
		else:
			self.state = NPC.STATE_MOVING
		super(NPC, self).hitplayer(clock, player)

	def hitenemy(self, clock, enemy):
		if self.collidex or self.collidey:
			self.state = NPC.STATE_STOPPED
		else:
			self.state = NPC.STATE_MOVING
		super(NPC, self).hitenemy(clock, enemy)

	def hitsurface(self, clock, surface):
		if self.collidex or self.collidey:
			self.state = NPC.STATE_STOPPED
		else:
			self.state = NPC.STATE_MOVING
		super(NPC, self).hitsurface(clock, surface)

	def movetowards(self, x, y):
		self.destination = (x,y)
		self.state = NPC.STATE_MOVING

	def update(self, clock, player, enemies, surfaces):
		#print "inner",self.rect.center[0], self.rect.center[1]
		vel = Vector2(0, 0)
		vel.x = self.destination[0] - self.rect.centerx
		vel.y = self.destination[1] - self.rect.centery
		self.vel = vel.normalized() * NPC_SPEED

		super(NPC, self).update(clock, player, enemies, surfaces)

