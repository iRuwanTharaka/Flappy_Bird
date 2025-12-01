"""Configuration constants and settings for the Flappy Bird game."""
import pygame
import os

# Screen settings
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
FPS = 60

# Initialize pygame fonts
pygame.font.init()
FONT = pygame.font.SysFont('Bauhaus 93', 60)
SMALL_FONT = pygame.font.SysFont('Arial', 32)
LARGE_FONT = pygame.font.SysFont('Arial', 72)
TINY_FONT = pygame.font.SysFont('Arial', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
GRAY = (128, 128, 128)

# Backend API Configuration
API_BASE_URL = "http://localhost:3000/api"

# Game settings
SCROLL_SPEED = 4
PIPE_GAP = 150
PIPE_FREQUENCY = 1500
GROUND_HEIGHT = 768

# Heart puzzle settings
HEART_TIME_LIMIT = 30  # seconds
HEART_PUZZLE_API_URL = "https://marcconrad.com/uob/heart/api.php"

# Image paths - using relative paths from the game module directory
_GAME_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_GAME_DIR)
_IMG_DIR = os.path.join(_PARENT_DIR, 'img')

IMAGE_PATHS = {
    'bg': os.path.join(_IMG_DIR, "bg.png"),
    'ground': os.path.join(_IMG_DIR, "ground.png"),
    'restart': os.path.join(_IMG_DIR, "restart.png"),
    'pipe': os.path.join(_IMG_DIR, "pipe.png"),
    'bird': os.path.join(_IMG_DIR, "bird{}.png")  # Format with number 1-3
}

