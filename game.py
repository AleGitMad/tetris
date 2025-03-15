import pygame
import random
from piece import Piece, TETROMINOS, bottom, side
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

# Crea un oggetto font (Arial, 36 punti)
font = pygame.font.Font(None, 36)  # Usa None per il font di default

# Renderizza il testo (testo, anti-aliasing, colore)
text_surface = font.render("Hai perso!", True, RED)

# Ottieni il rettangolo del testo e posizionalo al centro
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

end = False

# Game loop
running = True
clock = pygame.time.Clock()

piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH // 2, 0, 30, random.choice(colors))
bottom = Piece(bottom, 0 + GRID_SIZE, HEIGHT, 30, RED)
obstacles.add(bottom)
all_pieces.add(piece)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if piece.rect.y < 0:
        # Disegna il testo sulla finestra
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        end = True

    if piece.collision == True and end == False:
        obstacles.add(piece)
        piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH // 2, 0, 30, random.choice(colors))
        all_pieces.add(piece)

    if end == False:
        piece.update(obstacles)
        screen.fill(BLACK)
        draw_grid()
        all_pieces.draw(screen)
        obstacles.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()