import util

class WorldLoader:
	north = {}
	south = {}
	east = {}
	west = {}
	def __init__(self, worldname):
		f = util.loadMap(worldname)
		lines = f.readlines()
		for line in lines:
			line = line.rstrip()
			if line is not "":
				args = line.split()
				key, N, S, E, W = line.split()
				self.north[key] = N
				self.south[key] = S
				self.east[key] = E
				self.west[key] = W
