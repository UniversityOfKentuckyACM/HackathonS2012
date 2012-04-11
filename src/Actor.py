
import pygame
import os
import util
from Vector2 import Vector2
from config import *

class Actor(pygame.sprite.Sprite):
	"""
		Sprite class for pygame library
		Largely inspired by Chimp Tutorial
		www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
	"""

	def __init__(self, imageFile = None, colorKey = None):
		"""
			If supplied with an image load it. Also initialize velocity to (0,0).
		"""
		pygame.sprite.Sprite.__init__(self)

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

	def nextpos(self):
		"""
			Generate next rectangles from current velocity
		"""
		return self.rect.move(self.vel.x, 0), self.rect.move(0, self.vel.y)

	def collide(self, env):
		"""
			Return whether the object collides in x or y direction
		"""
		rectangles = [x.rect for x in env]
		xpos, ypos = self.nextpos()
		xcollide = xpos.collidelist(rectangles) != -1
		ycollide = ypos.collidelist(rectangles) != -1
		return xcollide, ycollide

	def update(self, *args):
		"""
			Move rect+image (vel[0], vel[1]) pixels
		"""

		if len(args):
			environment = args[0]
			collidex, collidey = self.collide(environment)
			if collidex:
				self.vel.x = 0
			if collidey:
				self.vel.y = 0
		self.rect.move_ip(self.vel.x, self.vel.y)

