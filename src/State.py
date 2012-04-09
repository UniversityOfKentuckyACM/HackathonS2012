import pygame

class State:
	def __init__(self, main):
		# transition from another state
		self.main = main
		
	def __del__(self):
		# transition to another state
		pass
		
	def update(self):
		# update 
		self.handleEvent()
		self.draw()
	
	def handleEvent(self):
		# handle events
		pass
		
	def draw(self):
		# draw group stuff
		pygame.display.flip()
