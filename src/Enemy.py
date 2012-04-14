__all__ = ["Enemy"]

import pygame
import util
import NPC

from Vector2 import Vector2

import config
import GameState

class Enemy(NPC.NPC):
	def __init__(self, gameState, x, y, name):
		super(Enemy, self).__init__(gameState, x, y, name)
		self.alive = True
		self.health = 4

	def update(self, clock, environment):
		#check if dead
		if (self.health <= 0):
			self.alive = False
			
		super(Enemy, self).update(clock, environment)

	def damaged(self, damage):
		health -= damage

	def attack(self, target, damage):
		target.damaged(damage)
