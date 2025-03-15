import pygame
import random
from piece import Piece, TETROMINOS
from dimensions import *

# Inizializza Pygame
pygame.init()

# Disegna la griglia
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (0, y), (WIDTH, y), 1)

all_pieces = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()

piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH // 2, 0, 30, random.choice(colors))
all_pieces.add(piece)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.K_SPACE:
            piece.on_ground()

    # Things to do

    piece.update(obstacles)
    screen.fill(BLACK)
    draw_grid()
    all_pieces.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()