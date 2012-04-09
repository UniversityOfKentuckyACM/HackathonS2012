
import util

class Map:
	NUM_ROWS = 24
	NUM_COLS = 28

	mapName = "map"
	aliases = {}
	atLayer = []
	belowLayer = []
	entities = []
	
	def getEntities(self):
		return self.entities
	
	def getAtLayer(self):
		return self.atLayer
	
	def getBelowLayer(self):
		return self.belowLayer
	
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
		for y in range(Map.NUM_ROWS):
			self.atLayer.append(['.'] * Map.NUM_COLS)
			self.belowLayer.append(['.'] * Map.NUM_COLS)
		
		f = util.loadMap(mapName)
		
		contents = f.readlines()
		contents = self.clean(contents)
		
		lineIndex = 0
		
		self.mapName = contents[lineIndex]
		
		lineIndex = lineIndex + 1 # the [RSC] tag
		lineIndex = lineIndex + 1 # move to first resource
		
		while contents[lineIndex] != "[AT]":
			pair = contents[lineIndex].split(' ')
			self.aliases[pair[0]]=pair[1]
			lineIndex = lineIndex + 1 # move to next pair or [AT] tag
		
		for y in range(24):
			lineIndex = lineIndex + 1
			for x in range(28):
				self.atLayer[y][x] = contents[lineIndex][x]
		
		lineIndex = lineIndex + 1 # the [BELOW] tag
		
		for y in range(24):
			lineIndex = lineIndex + 1
			for x in range(28):
				self.belowLayer[y][x] = contents[lineIndex][x]
		
		lineIndex = lineIndex + 1 # the [ENTITY] tag
		lineIndex = lineIndex + 1 # move to first entity
		
		while lineIndex < len(contents):
			self.entities.append(contents[lineIndex].split(' '))
			lineIndex = lineIndex + 1

