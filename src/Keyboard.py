import sys
import pygame.locals as constants

class Keymap(object):
	def __init__(self, **kwargs):
		self.codes = set()
		for key in kwargs:
			if hasattr(self, key):
				raise Exception("Duplicate action '%s' in keymap" % key)
			setattr(self, key, kwargs[key])
			self.codes.add(kwargs[key])
		self.kwargs = kwargs

	def __contains__(self, code):
		return code in self.codes

	def __iter__(self):
		return iter(self.codes)

	def __str__(self):
		return "Keymap: " + ", ".join("%s = %s" % (key, value) for (key, value) in self.kwargs.iteritems())

class Keyboard(object):
	def __init__(self, keymap):
		table = vars(constants)
		self.keys = dict((key, table[key]) for key in table if key.startswith('K_'))
		self.lo = min(self.keys.values())
		self.hi = max(self.keys.values())
		self.pressed = [False] * (self.hi - self.lo)
		self.keymap = keymap
		for code in keymap:
			if not self.iskey(code):
				raise Exception("Bad keymap: %s (%s) not available on keyboard" % (key, keymap[key]))

	# Is code a valid key number?
	def iskey(self, code):
		return self.lo <= code <= self.hi

	# Find code in keymap and return index into pressed vector
	def decode(self, code):
		if code not in self.keymap:
			raise Exception("Code %s not defined in keymap. See config.py." % code)
		return code - self.lo

	# Register key up or down in pressed vector
	def handle(self, event):
		if event.type == constants.KEYDOWN and self.iskey(event.key):
			self.pressed[event.key - self.lo] = True
			if event.key == constants.K_ESCAPE:
				sys.exit(0)
		if event.type == constants.KEYUP and self.iskey(event.key):
			self.pressed[event.key - self.lo] = False

	# See if key is down.
	def down(self, code):
		return self.pressed[self.decode(code)]

	# See if key is down. If it is, "unpress" it until next event.
	def downup(self, code):
		decoded = self.decode(code)
		down = self.pressed[decoded]
		if down:
			self.pressed[decoded] = False
		return down

	# See if key is up
	def up(self, code):
		return not self.pressed[self.decode(code)]

