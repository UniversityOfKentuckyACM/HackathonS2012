__all__ = ["Collider"]

import pygame
import util
import Actor
from Vector2 import Vector2

class Collider(Actor.Actor):
	def __init__(self):
		super(Collider, self).__init__()
		self.collidex = self.collidey = False

	def nextpos(self):
		"""
			Generate next rectangles from current velocity
		"""
		return self.rect.move(self.vel.x, 0), self.rect.move(0, self.vel.y)

	def collide(self, environment):
		"""
			Decide whether the object collides in x or y direction
		"""
		xpos, ypos = self.nextpos()
		self.collidex = xpos.collidelist(environment) != -1
		self.collidey = ypos.collidelist(environment) != -1

	def update(self, clock, environment, dies):
		"""
			Move unless collisions prevent one from doing so
		"""
		self.collide(environment)
		if self.collidex:
			self.vel.x = 0
		if self.collidey:
			self.vel.y = 0
		if (self.collidex or self.collidey) and dies:
			self.kill()
		super(Collider, self).update(clock)

