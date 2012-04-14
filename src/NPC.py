__all__ = ["NPC"]

import math
import pygame.sprite
import Collider
import util

from Vector2 import Vector2

import config

UP, DOWN, LEFT, RIGHT = range(4)
NPC_SPEED = 2
STATE_STOPPED = 0
STATE_MOVING = 1
NPC_SPEED = 2

class NPC(Collider.Collider):
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
		self.state = STATE_STOPPED
		self.destination = None

	def movetowards(self, x, y):
		self.destination = (x,y)
		self.state = STATE_MOVING
		
	def update(self, clock, environment):
		print "inner",self.rect.center[0], self.rect.center[1]
		
		if self.state == STATE_MOVING:
			if self.sqDistanceFrom(self.destination) < 4:
				self.vel.x = 0
				self.vel.y = 0
				self.state = STATE_STOPPED
			else:
				vel = Vector2(0, 0)
				vel.x = self.destination[0] - self.rect.center[0]
				vel.y = self.destination[1] - self.rect.center[1]
				
				self.vel = vel.normalized() * NPC_SPEED
				#self.setImage(self.images[self.direction])
				
			assert(self.destination != None)
			super(NPC, self).update(clock, environment, False)
