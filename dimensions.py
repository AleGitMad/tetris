import pygame
import random

# Dimensioni finestra
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS = 10
ROWS = 20
CELL_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colori
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREY = (50, 50, 50)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]