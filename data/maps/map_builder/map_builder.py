import os

def newLayer():
	layer = list()
	sVal = 0
	while (sVal < 24):
		tLay = list()	
		tVal = 0
		while (tVal < 28):
			tLay.append('.')
			tVal = tVal + 1
		layer.append(tLay)
		sVal = sVal + 1
	return layer

rsc_list = list()
rsc_list.append('[RSC]')
rscListBase = list()
layer_at = newLayer()
layer_under = newLayer()
entity_list = list()
entity_list.append('[ENTITY]')

def addRsc(char):
	if rscListBase.count(char) < 1:
		rscListBase.append(char)
		if (char == 'D'):
			rsc_list.append('D dungeonDoor.png')
		elif (char == 'd'):
			rsc_list.append('d dirt.png')
		elif (char == 'G'):
			rsc_list.append('G grassDead.png')
		elif (char == 'g'):
			rsc_list.append('g grass.png')
		elif (char == 'm'):
			rsc_list.append('r rockyMountain.png')
		elif (char == 'P'):
			rsc_list.append('P treeTop.png')
		elif (char == 'p'):
			rsc_list.append('p treeBottom.png')
		elif (char == 'R'):
			rsc_list.append('R rubbleDead.png')
		elif (char == 'r'):
			rsc_list.append('r rubble.png')
		elif (char == 'S'):
			rsc_list.append('S sandDead.png')
		elif (char == 's'):
			rsc_list.append('s sand.png')
		elif (char == 'W'):
			rsc_list.append('W waterToxic.png')
		elif (char == 'w'):
			rsc_list.append('w water.png')
		elif (char == 'X'):
			rsc_list.append('X waterToxicWithStone.png')
		elif (char == 'x'):
			rsc_list.append('x stone.png')
		elif (char == 'Y'):
			rsc_list.append('Y treeDyingTop.png')
		elif (char == 'y'):
			rsc_list.append('y treeDyingBottom.png')
		elif (char == '@'):
			rsc_list.append('@ impassableRockDead.png')
		elif (char == '#'):
			rsc_list.append('# wall.png')
		elif (char == '%'):
			rsc_list.append('% snowyMountain.png')
		elif (char == '*'):
			rsc_list.append('* impassableRock.png')
		elif (char == '_'):
			rsc_list.append('_ ground.png')

def drawLayer(layer, drawType, char, x1=0, y1=0, x2=0, y2=0):
	addRsc(char)
	fill = False
	if drawType == 'all':
		fill = True
		x1 = 0
		x2 = 28
		y1 = 0
		y2 = 24
	elif drawType == 'box':
		fill = False
	elif drawType == 'fbox':
		fill = True
	if drawType == 'all' or drawType == 'box' or drawType == 'fbox':
		y = y1
		while (y < y2):
			if (fill or (y == y1) or (y == y2-1)):
				x = x1
				while (x < x2):
					layer[y][x] = char
					x = x + 1
			else:
				layer[y][x1] = char
				layer[y][x2-1] = char
			y = y + 1
	elif drawType == 'point':
		layer[y1][x1] = char
	elif drawType == 'hline':
		x = x1
		while (x < x2):
			layer[y1][x] = char
			x = x + 1
	elif drawType == 'hline2':
		x = x1
		while (x < x2):
			layer[y1][x] = char
			layer[y1+1][x] = char
			x = x + 1
	elif drawType == 'vline':
		y = y1
		y2 = x2
		while (y < y2):
			layer[y][x1] = char
			y = y + 1
	elif drawType == 'vline2':
		y = y1
		y2 = x2
		while (y < y2):
			layer[y][x1] = char
			layer[y][x1+1] = char
			y = y + 1
	else:
		print '@' + ': warning - could not find draw type'
	return

def printLayer(layer, layerName='[]'):
	print layerName
	for each in layer:
		line = ""
		for eachChr in each:
			line = line + eachChr
		print line

def printList(lis):
	for each in lis:
		print each

def main(planName):
	lineNumber = 1
	mapName = ' '
	planFile = open(planName, 'rb')
	lines = planFile.readlines()
	layer_use = list()
	layer_use.append('Nought')
	atMode = False
	bottomMode = False
	for line in lines:
		if (line !='#B\n') and (line != '#@\n'):
			words = line.split()
			title = words[0]
			title_sub = words[1]
			if words.count(';;') >= 1:
				if (title == '#$'):
					i = 2
					nameString = words[1]
					while (words[i] != ';;'):
						nameString = nameString + ' ' + words[i]
						i = i + 1
					mapName = nameString
				elif (title == 'door') and (words.index(';;') > 2):
					x = int(words[1])
					y = int(words[2])
					layer_at[y][x] = 'D'
					addRsc('D')
					appStr = 'door dungeonDoor.png ' + str(x * 32) + ' ' + str(y * 32) + ' ' + words[3]
					entity_list.append(appStr)
				elif ((title == 'dead_tree') and (words.index(';;') > 2)):
					x = int(words[1])
					y = int(words[2])
					layer_at[y][x] = 'Y'
					layer_at[y+1][x] = 'y'
					addRsc('Y')
					addRsc('y')
				elif ((title == 'dead') and (title_sub == 'tree') and (words.index(';;') > 3)):
					x = int(words[2])
					y = int(words[3])
					layer_at[y][x] = 'Y'
					layer_at[y+1][x] = 'y'
					addRsc('Y')
					addRsc('y')
				elif (title == 'tree') and (words.index(';;') > 2):
					x = int(words[1])
					y = int(words[2])
					layer_at[y][x] = 'P'
					layer_at[y+1][x] = 'p'
					addRsc('P')
					addRsc('p')
				elif (layer_use[0] != 'Nought'):
					if words.index(';;') < 4:
						drawLayer(layer_use, words[0], words[1])
					elif words.index(';;') == 4:
						drawLayer(layer_use, words[0], words[1], int(words[2]), int(words[3]))
					elif words.index(';;') == 5:
						drawLayer(layer_use, words[0], words[1], int(words[2]), int(words[3]), int(words[4]))
					else:
						drawLayer(layer_use, words[0], words[1], int(words[2]), int(words[3]), int(words[4]), int(words[5]))
			else:
				print '@line ' + str(lineNumber) + ': fatal - no \';;\' to signify end of line\n\n'
		else:
			layer_use = list()
			layer_use.append('Nought')
			if (line == '#B\n'):
				layer_use = layer_under
			if (line == '#@\n'):
				layer_use = layer_at
		lineNumber = lineNumber + 1
	print mapName
	printList(rsc_list)
	printLayer(layer_at, '[AT]')
	printLayer(layer_under, '[UNDER]')
	printList(entity_list)
	return

main('sample.map.plan')
