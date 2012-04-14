__all__ = ["NPC"]

import math
import pygame.sprite
import Collider
import util

from Vector2 import Vector2

import config

UP, DOWN, LEFT, RIGHT = range(4)
NPC_SPEED = 8

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

	def movetowards(self, x, y, clock, environment):
		vel = Vector2(0, 0)
		if x < self.rect.left:
			self.direction = LEFT
			vel.x += 1
		if x > self.rect.right:
			self.direction = RIGHT
			vel.x -= 1
		if y < self.rect.top:
			self.direction = UP
			vel.y += 1
		if y > self.rect.bottom:
			self.direction = DOWN
			vel.y -= 1
		self.vel = vel.normalized() * NPC_SPEED
		self.setImage(self.images[self.direction])
		super(NPC, self).update(clock, environment, False)

""" n = NPC(3, 3, "Skeleton")
"""
"""
	self.movable
	self.images = [0] * 4
		self.NPC_IDLE_UP
		self.NPC_IDLE_DOWN
		self.NPC_IDLE_LEFT
		self.NPC_IDLE_RIGHT
"""
