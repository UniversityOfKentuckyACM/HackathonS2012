
import os
import sys
import util

class WorldLoader:
	"""
		Parse of *.world files. They are of the format:
			ROWS %d
			COLUMNS %d
			DIR %s
		Where DIR is the directory (relative) in which the necessary .map files 
		can be found. They are expected to be named MYROW_MYCOL.map
	"""

	ROWS = "ROWS"
	COLS = "COLUMNS"
	DIR = "DIR"

	def __init__(self, worldname):
		self.north = {}
		self.south = {}
		self.east = {}
		self.west = {}

		f = util.loadMap(worldname)
		for line in f:
			line = line.rstrip()
			id, val = line.split()
			if id == WorldLoader.ROWS:
				self.rows = int(val)
			elif id == WorldLoader.COLS:
				self.cols = int(val)
			elif id == WorldLoader.DIR:
				self.dir = val
			else:
				print "Error: unknown ID in %s -> \"%s\"" % (worldname, val)
				sys.exit(1)

		# Now now load map files. These really should be named i_j.map but are
		# actually j_i.map, presumably because of x_y.
		for i in range(self.rows):
			for j in range(self.cols):
				key = "%s_%s.map" % (i, j)
				key = os.path.join(self.dir, key)
				# key should now be "dir/i_j.map"

				# now determine filenames for N/S/E/W maps. This replaces the
				# old .world files
				if j > 0:
					self.north[key] = os.path.join(self.dir, "%d_%d.map" % (i, j-1))
				else:
					self.north[key] = None
				if j < self.rows - 1:
					self.south[key] = os.path.join(self.dir, "%d_%d.map" % (i, j+1))
				else:
					self.south[key] = None
				if j > 0:
					self.west[key] = os.path.join(self.dir, "%d_%d.map" % (i-1, j))
				else:
					self.west[key] = None
				if i < self.cols - 1:
					self.east[key] = os.path.join(self.dir, "%d_%d.map" % (i+1, j))
				else:
					self.east[key] = None
				
