__all__ = ["Magic"]

from Collider import Collider
import util

from Vector2 import Vector2
import config
import pygame.transform
import math

# Local settings
MAGIC_SPEED = 5
MAGIC_ATTACK_IMAGE = "fireballRight.png"
MAGIC_DAMAGE = 2

class Magic(Collider):
		'''
				Magic class for the magic attack
		'''
		loadedImage = False

		def __init__(self, x, y, direction, parent):
			super(Magic,self).__init__()
			self.dieoncollide = True
			self.parent = parent

			if not Magic.loadedImage:
				Magic.loadedImage,tmp = util.loadImage(MAGIC_ATTACK_IMAGE)

			self.setImage(Magic.loadedImage)
			self.setPos(x, y)
			self.setVel(direction.normalized() * MAGIC_SPEED)
			self.image = pygame.transform.rotate(self.image,270+360*(math.atan2(self.vel.x,self.vel.y)/6.28))

		#Use to find coordinates of mouse relative to current pos. Set Vector
		def magicPath(self):
				pass

		def damage(self, target):
			target.damaged(MAGIC_DAMAGE)

		def hitplayer(self, clock, player):
			if self.collidex or self.collidey:
				self.damage(player)
			super(Magic, self).hitplayer(clock, player)

		def hitenemy(self, clock, enemy):
			if self.collidex or self.collidey:
				self.damage(enemy)
			super(Magic, self).hitenemy(clock, enemy)

		def update(self, clock, player, enemies, surfaces):
			super(Magic,self).update(clock, player, enemies, surfaces)

			#Kill magic object if it reaches the windows bounds.
			if self.rect.top > config.HEIGHT or self.rect.top < 0 or self.rect.right < 64 or self.rect.right > config.WIDTH - 64:
				self.kill()

