import sys
import pygame.locals as constants

class Keyboard(object):
	def __init__(self, keymap):
		table = vars(constants)
		self.keys = dict((key, table[key]) for key in table if key.startswith('K_'))
		self.lo = min(self.keys.values())
		self.hi = max(self.keys.values())
		self.pressed = [False] * (self.hi - self.lo)
		self.keymap = keymap
		for key in keymap:
			if not self.iskey(keymap[key]):
				raise Exception("Bad keymap: %s (%s) not available on keyboard" % (key, keymap[key]))

	# Is code a valid key number?
	def iskey(self, code):
		return self.lo <= code <= self.hi

	# Is action string in keymap?
	def decode(self, action):
		if action not in self.keymap:
			raise Exception("Action '%s' not defined in keymap. See config.py" % action)
		return self.keymap[action] - self.lo

	# Register key up or down in pressed vector
	def handle(self, event):
		if event.type == constants.KEYDOWN and self.iskey(event.key):
			self.pressed[event.key - self.lo] = True
			if event.key == constants.K_ESCAPE:
				sys.exit(0)
		if event.type == constants.KEYUP and self.iskey(event.key):
			self.pressed[event.key - self.lo] = False

	# See if key is down.
	def down(self, action):
		return self.pressed[self.decode(action)]

	# See if key is down. If it is, "unpress" it.
	def downup(self, action):
		code = self.decode(action)
		down = self.pressed[code]
		if down:
			self.pressed[code] = False
		return down

	# See if key is up
	def up(self, action):
		return not self.pressed[self.decode(action)]

