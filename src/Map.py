
import util

class Map(object):
	NUM_ROWS = 24
	NUM_COLS = 28

	def getEntities(self):
		return self.entities

	def getAtLayer(self):
		return self.atLayer

	def getBelowLayer(self):
		return self.belowLayer

	def getOverLayer(self):
		return self.overLayer

	def clean(self, contents):
		'''
			Remove comments and newlines from map file.
		'''
		cleanContents = []
		for line in contents:
			line = line.strip()
			if line != "":
				if not line.startswith('\''):
					cleanContents.append(line.split('\'')[0].strip())
		return cleanContents

	def __init__(self, mapName):
		self.aliases = {}
		self.atLayer = []
		self.belowLayer = []
		self.overLayer = []
		self.entities = []
		for y in range(Map.NUM_ROWS):
			blanks = ['.'] * Map.NUM_COLS
			self.atLayer.append(blanks[:])
			self.belowLayer.append(blanks[:])
			self.overLayer.append(blanks[:])

		f = util.loadMap(mapName)
		lines = self.clean(f.readlines())
		f.close()
		end = len(lines)
		lineIndex = 0
		self.mapName = lines[lineIndex]
		lineIndex += 1
		section = lines[lineIndex]

		# Required RSC section
		if section != "[RSC]":
			raise Exception("Missing RSC Header in map file '%s'" % mapName)
		lineIndex += 1

		while lineIndex < end and lines[lineIndex] != "[AT]":
			line = lines[lineIndex]
			if line:
				alias, image = line.split()
				self.aliases[alias] = image
			lineIndex += 1

		# Required AT
		if lineIndex >= end or lines[lineIndex] != "[AT]":
			raise Exception("No [AT] group in map file '%s'" % mapName)
		lineIndex += 1

		for y in range(Map.NUM_ROWS):
			for x in range(Map.NUM_COLS):
				self.atLayer[y][x] = lines[lineIndex][x]
			lineIndex += 1

		# Required UNDER
		while lineIndex < end and lines[lineIndex] != "[UNDER]":
			lineIndex += 1
		if lineIndex >= end or lines[lineIndex] != "[UNDER]":
			raise Exception("No [UNDER] group in map file '%s'" % mapName)
		lineIndex += 1

		for y in range(Map.NUM_ROWS):
			for x in range(Map.NUM_COLS):
				self.belowLayer[y][x] = lines[lineIndex][x]
			lineIndex += 1

		while lineIndex < end and lines[lineIndex] not in ("[ENTITY]", "[OVER]"):
			lineIndex += 1

		# Optional OVER
		if lineIndex < end and lines[lineIndex] == "[OVER]":
			lineIndex += 1
			for y in range(Map.NUM_ROWS):
				for x in range(Map.NUM_COLS):
					self.overLayer[y][x] = lines[lineIndex][x]
				lineIndex += 1

		# Optional ENTITY
		while lineIndex < end and lines[lineIndex] not in "[ENTITY]":
			lineIndex += 1

		if lineIndex < end and lines[lineIndex] == "[ENTITY]":
			lineIndex += 1
			while lineIndex < end:
				self.entities.append(lines[lineIndex].split(' '))
				lineIndex += 1

