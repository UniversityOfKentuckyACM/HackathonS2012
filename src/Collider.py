__all__ = ["Collider"]

import pygame
import util
import Actor
from Vector2 import Vector2

class Collider(Actor.Actor):
	def __init__(self):
		super(Collider, self).__init__()
		self.collidex = self.collidey = False
		self.parent = None
		self.dieoncollide = False

	def nextpos(self):
		"""
			Generate next rectangles from current velocity
		"""
		return self.rect.inflate(-5, -5).move(self.vel.x, 0), self.rect.inflate(-5, -5).move(0, self.vel.y)

	def collide(self, xpos, ypos, other):
		"""
			Decide whether the object collides in x or y direction
		"""
		if self is not other and (self.parent is None or self.parent is not other):
			self.collidex = xpos.colliderect(other.rect)
			self.collidey = ypos.colliderect(other.rect)

	def stop(self):
		if self.collidex:
			self.vel.x = 0
		if self.collidey:
			self.vel.y = 0
		if (self.collidex or self.collidey) and self.dieoncollide:
			self.kill()

	def hitplayer(self, clock, player):
		self.stop()

	def hitenemy(self, clock, enemy):
		self.stop()

	def hitsurface(self, clock, surface):
		self.stop()

	def update(self, clock, player, enemies, surfaces):
		"""
			Move unless collisions prevent one from doing so
		"""

		xpos, ypos = self.nextpos()
		self.collide(xpos, ypos, player)
		self.hitplayer(clock, player)

		for enemy in enemies:
			self.collide(xpos, ypos, enemy)
			self.hitenemy(clock, player)

		for surface in surfaces:
			self.collide(xpos, ypos, surface)
			self.hitsurface(clock, surface)

		super(Collider, self).update(clock)

