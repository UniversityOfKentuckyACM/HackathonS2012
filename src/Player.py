import math
import pygame.sprite
import Actor
import util

from Vector2 import Vector2
from Magic import Magic

from config import *

class Player(Actor.Actor):
	'''
		Player class. images is a list of images for each direction. We may need
		to alter this to support animation.
	'''
	def __init__(self,gameState):
		super(Player,self).__init__()
		
		# load all images
		# up, down, left, right
		self.images = [0] * 4
		self.images[0], self.rect = util.loadImage(PLAYER_IDLE_UP, -1)
		self.images[1], self.rect = util.loadImage(PLAYER_IDLE_DOWN, -1)
		self.images[2], self.rect = util.loadImage(PLAYER_IDLE_LEFT, -1)
		self.images[3], self.rect = util.loadImage(PLAYER_IDLE_RIGHT, -1)
		
		# 0 = up, 1 = down, 2 = left, 3 = right
		self.direction = 0
		
		# assign image and position
		self.setImage(self.images[self.direction])
		self.setPos(START_X, START_Y)

		# load sword
		self.swordLeft        = pygame.sprite.Sprite()
		self.swordLeft.image,self.swordLeft.rect  = util.loadImage("swordSwingLeft.png")
		self.swordUp          = pygame.sprite.Sprite()
		self.swordUp.image,self.swordUp.rect    = util.loadImage("swordSwingUp.png")
		self.swordRight       = pygame.sprite.Sprite()
		self.swordRight.image,self.swordRight.rect = util.loadImage("swordSwingRight.png")
		self.swordDown        = pygame.sprite.Sprite()
		self.swordDown.image,self.swordDown.rect  = util.loadImage("swordSwingDown.png")
	
		self.gameState = gameState
	
	# Orient player with mouse
	def orient(self, mousePos):
		loc = mousePos - Vector2(self.getPos())
		angle = math.atan2(loc[1],loc[0])
		mag = math.fabs(angle)
		
		# if we're facing to the right
		if mag < math.pi / 4:
			self.setDir(3)
		# move left
		elif mag > 3*math.pi / 4:
			self.setDir(2)
		# either up or down
		else:
			if angle < 0:
				self.setDir(0)
			else:
				self.setDir(1)
	
	def setDir(self, newDir):
		self.direction = newDir
		self.image = self.images[self.direction]
	
	def collideWall(self, wall):
		# collision on the top of charcter
		if self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.top and self.vel[1]<0:
			self.vel -= Vector2(0,0)
			self.rect.top = wall.rect.bottom
		# collision on the bottom of character
		if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.bottom and self.vel[1]>0:
                        self.vel -= Vector2(0,0)
                        self.rect.bottom = wall.rect.top
                # collision on the right side of character
                if self.rect.right > wall.rect.left and self.rect.left < wall.rect.right and self.vel[0]>0:
                        self.vel -= Vector2(0,0)
                        self.rect.right = wall.rect.left
                # collision on the left side of character
                if self.rect.left < wall.rect.right and self.rect.right > wall.rect.left and self.vel[0]<0:
                        self.vel -= Vector2(0,0)
                        self.rect.left = wall.rect.right
	
	def move(self, m):
		'''
			Press a key and add to our velocity vector
		'''
		if m == -1:
			self.vel = Vector2(0,0)
		elif m == 0:
			self.vel += Vector2(0,-1) * PLAYER_SPEED
		elif m == 1:
			self.vel += Vector2(0,1) * PLAYER_SPEED
		elif m == 2:
			self.vel += Vector2(-1,0) * PLAYER_SPEED
		elif m == 3:
			self.vel += Vector2(1,0) * PLAYER_SPEED
	
	def unMove(self, m):
		'''
			Once a key is released, remove that from velocity vector.
		'''
		if m == 0:
			self.vel -= Vector2(0,-1) * PLAYER_SPEED
		elif m == 1:
			self.vel -= Vector2(0,1) * PLAYER_SPEED
		elif m == 2:
			self.vel -= Vector2(-1,0) * PLAYER_SPEED
		elif m == 3:
			self.vel -= Vector2(1,0) * PLAYER_SPEED
	
	# TODO: FIX THIS
	def swingSword(self):
		'''
			When left mouse is pressed, sword is pushed out
		'''
		if self.direction == 0:
		 	self.swordUp.rect.bottomleft = self.rect.topleft
			self.swordUp.add(self.gameState.playerGroup)
		elif self.direction == 1:
		 	self.swordDown.rect.topleft = self.rect.bottomleft
			self.swordDown.add(self.gameState.playerGroup)
		elif self.direction == 2:
		 	self.swordLeft.rect.topright = self.rect.topleft
			self.swordLeft.add(self.gameState.playerGroup)
		elif self.direction == 3:
		 	self.swordRight.rect.topleft = self.rect.topright
			self.swordRight.add(self.gameState.playerGroup)

    	# TODO: Add to this
    	def shootBow(self):
        	'''
        	When right mouse is pressed, arrow is fire infront of character
		'''
        	print "Arrow Fired"
        
   	# TODO: Add to this
   	def useMagic(self):
        	'''
        	When space bar is pressed, magic is thrown towards the mouse pointer
        	Or infront of the character *Choice*
        	'''
        	pos = self.rect.center
        	self.magi = Magic(pos[0],pos[1])

        	self.magi.add(self.gameState.playerGroup)
        	
	
	def update(self):
		super(Player,self).update()

		# Check to see if we have touched edge of the screen
		if self.rect.left < TILEX * 2:
			self.gameState.nextMap("left", self.getPos())
		elif self.rect.right > WIDTH - (TILEX*2):
			self.gameState.nextMap("right", self.getPos())
		elif self.rect.top < 0:
			self.gameState.nextMap("up", self.getPos())
		elif self.rect.bottom > HEIGHT:
			self.gameState.nextMap("down", self.getPos())
