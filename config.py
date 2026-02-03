import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# FPS / Speed (Levels)
DIFFICULTY = {
    "EASY": 10,
    "MEDIUM": 15,
    "HARD": 25
}

# Win Condition
TARGET_LENGTH = {
    "EASY": 10,
    "MEDIUM": 20,
    "HARD": 30
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (200, 200, 50)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Snake Colors Options
SNAKE_COLORS = {
    "Green": GREEN,
    "Blue": BLUE,
    "Yellow": YELLOW,
    "Red": RED,
    "White": WHITE,
    "Black": BLACK
}

# Themes
THEMES = {
    "DARK": {
        "background": (30, 30, 30),
        "text": (240, 240, 240),
        "grid": (40, 40, 40),
        "ui_bg": (50, 50, 50),
        "ui_border": (100, 100, 100),
        "input_bg": (70, 70, 70),
        "input_text": (255, 255, 255)
    },
    "LIGHT": {
        "background": (240, 240, 240),
        "text": (20, 20, 20),
        "grid": (220, 220, 220),
        "ui_bg": (200, 200, 200),
        "ui_border": (150, 150, 150),
        "input_bg": (255, 255, 255),
        "input_text": (0, 0, 0)
    }
}
