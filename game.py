import pygame
import random
from piece import Piece, TETROMINOS, bottom
from dimensions import *
from map import Map

# Inizializza Pygame
pygame.init()

# Disegna la griglia
def draw_grid():
    for x in range(0, WIDTH_G, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (x, 0), (x, HEIGHT), 1)
    for y in range(50, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GREY, (0, y), (WIDTH, y), 1)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH_G, START))
    pygame.draw.rect(screen, BLACK, (WIDTH_G, 0, WIDTH, HEIGHT))

all_pieces = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Crea un oggetto font (Arial, 36 punti)
font = pygame.font.Font(None, 36)  # Usa None per il font di default

# Renderizza il testo (testo, anti-aliasing, colore)
text_surface = font.render("Hai perso!", True, RED)

# Ottieni il rettangolo del testo e posizionalo al centro
text_rect = text_surface.get_rect(center=(WIDTH_G // 2, HEIGHT // 2))

end = False

# Game loop
running = True
clock = pygame.time.Clock()

game_map = Map(HEIGHT // GRID_SIZE, WIDTH_G // GRID_SIZE, GRID_SIZE)

piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH_G // 2, START - GRID_SIZE, 30, random.choice(colors))
bottom = Piece(bottom, 0 + GRID_SIZE, HEIGHT, 30, RED)
obstacles.add(bottom)
all_pieces.add(piece)
topCollision = HEIGHT

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_SPACE:
            piece.on_ground()
        piece.handle_key_events(event)
    
    for sprite in obstacles.sprites():
        if sprite.rect.y < topCollision:
            topCollision = sprite.rect.y
    
    if topCollision <= START:
        # Disegna il testo sulla finestra
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        end = True

    if piece.collision == True and end == False:
        game_map.add_piece(piece)
        cleared = game_map.clear_full_rows()
        
        obstacles.add(piece)
        piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH_G // 2, START - GRID_SIZE, 30, random.choice(colors))
        all_pieces.add(piece)

    if end == False:
        piece.update(obstacles, game_map)
        screen.fill(BLACK)
        draw_grid()
        # game_map.draw(screen)  # per debug visivo delle righe occupate
        all_pieces.draw(screen)
        obstacles.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()