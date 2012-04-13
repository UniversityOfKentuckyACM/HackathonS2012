# Configuration variables to be used by rest of game

import pygame.locals as constants

# Player actions mapped to key values
keymap = {
	"UP":			constants.K_w,
	"DOWN":			constants.K_s,
	"LEFT":			constants.K_a,
	"RIGHT":		constants.K_d,
	"MAGIC":		constants.K_k,
	"START":		constants.K_RETURN,

	# Testing only
	"HEALTHUP":		constants.K_UP,
	"HEALTHDOWN":	constants.K_DOWN,
}

# Global keyboard object
from Keyboard import Keyboard
keyboard = Keyboard(keymap)

# Video configuration
WIDTH = 1024
HEIGHT = 768
IS_FULLSCREEN = False
FRAME_RATE = 60

# Standard size of sprite tiles
TILEX = 32
TILEY = 32

# Points us to the name of the world file
WORLD_NAME = "tygra.world"

# Data Directories
GAME_IMAGES = "images"
GAME_SOUNDS = "sounds"
GAME_MAPS = "maps"

