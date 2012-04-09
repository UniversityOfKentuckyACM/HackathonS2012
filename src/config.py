# Configuration variables to be used by rest of game
import os
from pygame.locals import *

WIDTH = 1024
HEIGHT = 768
IS_FULLSCREEN = False
FRAME_RATE = 60
TILEX = 32
TILEY = 32

GAME_TITLE = "Hackathon!"

# up, down, left right
MOVEMENT_KEYS = [K_w, K_s, K_a, K_d]

MAGIC_ATTACK_KEY = K_SPACE

GAME_IMAGES = "images"
GAME_SOUNDS = "sounds"
GAME_MAPS = "maps"

START_X = WIDTH / 2
START_Y = HEIGHT / 2

PLAYER_SPEED = 8
MAGIC_SPEED = (3,-3)

# Player up, down, left, right sprites
PLAYER_IDLE_IMAGES = ["characterUp1.png", "characterDown1.png", "characterLeft1.png", "characterRight1.png"]
PLAYER_IDLE_UP = PLAYER_IDLE_IMAGES[0]
PLAYER_IDLE_DOWN = PLAYER_IDLE_IMAGES[1]
PLAYER_IDLE_LEFT = PLAYER_IDLE_IMAGES[2]
PLAYER_IDLE_RIGHT = PLAYER_IDLE_IMAGES[3]

#Weapons sprites
MAGIC_ATTACK_IMAGE = "fireballRight.png"

START_MENU = "START"
PLAY = "PLAY"
