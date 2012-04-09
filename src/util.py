import os,pygame

from pygame.locals import *
from config import *

## LOAD UTILITIES ##
data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    '''
		Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''
		Open a file in the data directory.
		"mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

## END LOAD UTILITIES ##

def loadMap(mapFile):
	path = os.path.join(GAME_MAPS, mapFile)
	path = filepath(path)
	return load(path)

# Thank you chimp tutorial!
def loadImage(imageFile, colorKey=None):
	path = os.path.join(GAME_IMAGES, imageFile)
	path = filepath(path)
	try:
		image = pygame.image.load(path)
	except pygame.error, message:
		print "Error loading image:", imageFile
		raise SystemExit, message
	
	# convert for speed and grab rect for collisions
	image = image.convert_alpha()
	rect = image.get_rect()
	
	# handle colorKey
	if colorKey is not None:
		if colorKey is -1:
			colorKey = image.get_at((0,0))
		image.set_colorkey(colorKey, RLEACCEL)

	return image, rect
	
def loadSound(name):
	path = os.path.join(GAME_SOUNDS, name)
	path = filepath(path)
	class NoneSound:
		def play(self): pass
    	if not pygame.mixer or not pygame.mixer.get_init():
        	return NoneSound()
    
    	try:
        	sound = pygame.mixer.Sound(path)
    	except pygame.error, message:
        	print 'Cannot load sound:', path
        	raise SystemExit, message
    	return sound
