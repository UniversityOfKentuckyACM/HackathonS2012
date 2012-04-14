# Configuration variables to be used by rest of game

import pygame.locals as constants

# Global keyboard object
# use like `if keyboard.down(keymap.UP): ...`
from Keyboard import Keyboard, Keymap

# Map player actions to key codes
keymap = Keymap(
	UP    = constants.K_w,
	DOWN  = constants.K_s,
	LEFT  = constants.K_a,
	RIGHT = constants.K_d,
	MAGIC = constants.K_k,
	START = constants.K_RETURN,
	DUP   = constants.K_UP,
	DDOWN = constants.K_DOWN,
	DLEFT = constants.K_LEFT,
	DRIGHT = constants.K_RIGHT,
)


# Validate keymap and build keyboard object
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

