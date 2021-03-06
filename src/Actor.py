__all__ = ["Actor"]

import pygame
import os
import util
from Vector2 import Vector2
import config

class Actor(pygame.sprite.Sprite):
	"""
		Sprite class for pygame library
		Largely inspired by Chimp Tutorial
		www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
	"""

	def __init__(self, imageFile=None, colorKey=None, mapStart=[0,0]):
		"""
			If supplied with an image load it. Also initialize velocity to (0,0).
		"""
	
		pygame.sprite.Sprite.__init__(self)

		# [column, row] of which map screen player is in
		self.mapPos = mapStart

		if imageFile is not None:
			self.loadImage(imageFile, colorKey)

		# Velocity vector
		self.vel = Vector2(0,0)

	def computeRect(self,rect):
		self.image = pygame.Surface((rect.width,rect.height))
		self.rect = rect

	# largely tutorial's load_image method. Thanks!
	def loadImage(self, imageFile, colorKey=None):
		self.image, self.rect = util.loadImage(imageFile, colorKey)

	def setImage(self, newImage):
		self.image = newImage
		self.rect = self.image.get_rect()

	def setPos(self, newX, newY):
		self.rect.center = (newX, newY)

	def setCornerPos(self, newX, newY):
		'''
			Assign top-left corner to (newX,newY)
		'''
		self.rect.left = newX
		self.rect.top = newY

	def getPos(self):
		return self.rect.center

	def getCornerPos(self):
		'''
			Return (x,y) of top-left corner
		'''
		return (self.rect.left, self.rect.top)

	def getRect(self):
		return self.rect

	def setVel(self, newVel):
		self.vel = newVel

	def getVel(self):
		return self.vel

	def sqDistanceFrom(self,other):
		return (other.rect.center[0] - self.rect.center[0])**2 +\
			(other.rect.center[1] - self.rect.center[1])**2
			
	def sqDistanceFrom(self,pos):
		return (pos[0] - self.rect.center[0])**2 +\
			(pos[1] - self.rect.center[0])**2

	def update(self, clock):
		"""
			Move rect+image (vel[0], vel[1]) pixels
		"""
		self.rect.move_ip(self.vel.x, self.vel.y)

