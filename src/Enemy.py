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
		self.ticks = 0

	def hitplayer(self, clock, player):
		if (self.collidex or self.collidey) and self.ticks == 0:
			self.attack(player, 1)
			self.ticks = pygame.time.get_ticks()
		elif self.ticks < 100000:
			self.ticks += pygame.time.get_ticks()
		else:
			self.ticks = 0
		super(Enemy, self).hitplayer(clock, player)

	def update(self, clock, player, enemies, surfaces):
		#check if dead
		if (self.health <= 0):
			self.alive = False
			self.remove(self.gamestate.enemyGroup)
			return
		self.movetowards(player.rect.centerx, player.rect.centery)
		super(Enemy, self).update(clock, player, enemies, surfaces)

	def damaged(self, damage):
		self.health -= damage

	def attack(self, target, damage):
		target.damaged(damage)

