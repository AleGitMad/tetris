import pygame
import random

# Inizializza Pygame
pygame.init()

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

# Disegna la griglia
for x in range(0, WIDTH, GRID_SIZE):
    pygame.draw.line(screen, DARK_GREY, (x, 0), (x, HEIGHT), 1)
for y in range(0, HEIGHT, GRID_SIZE):
    pygame.draw.line(screen, DARK_GREY, (0, y), (WIDTH, y), 1)

# Pezzi di Tetris (rotazioni incluse)
TETROMINOS = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "L": [[1, 0, 0], [1, 1, 1]],
    "J": [[0, 0, 1], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]]
}

class Piece(pygame.sprite.Sprite):
    def __init__(self, shape, x, y, block_size=30, color=(255, 255, 255)):
        super().__init__()
        self.shape = shape
        self.block_size = block_size
        self.color = color
        self.matrix = TETROMINOS[shape]  # Matrice del pezzo

        self.gravity_timer = pygame.time.get_ticks()  # Timer per la caduta

        # Calcola larghezza e altezza della superficie
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        self.image = pygame.Surface((cols * block_size, rows * block_size), pygame.SRCALPHA)

        # Disegna i blocchi sulla superficie
        for row in range(rows):
            for col in range(cols):
                if self.matrix[row][col] == 1:
                    pygame.draw.rect(self.image, color, (col * block_size, row * block_size, block_size, block_size))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Maschera per collisioni

    def rotate(self):
        """Ruota la matrice del Tetromino di 90°"""
        self.matrix = [list(row) for row in zip(*self.matrix[::-1])]
        
        # Ricrea la superficie con la nuova rotazione
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        self.image = pygame.Surface((cols * self.block_size, rows * self.block_size), pygame.SRCALPHA)
        
        for row in range(rows):
            for col in range(cols):
                if self.matrix[row][col] == 1:
                    pygame.draw.rect(self.image, self.color, (col * self.block_size, row * self.block_size, self.block_size, self.block_size))

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)  # Aggiorna la maschera di collisione

    def apply_gravity(self, obstacles):
        """Fa cadere il pezzo ogni tot millisecondi"""
        now = pygame.time.get_ticks()
        if now - self.gravity_timer > 500:  # Tempo in ms (500 ms = 0.5 sec)
            self.gravity_timer = now
            self.rect.y += self.block_size
            if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
                self.rect.y -= self.block_size  # Blocca il movimento se c'è una collisione

    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -self.block_size
        if keys[pygame.K_RIGHT]: dx = self.block_size
        if keys[pygame.K_DOWN]: dy = self.block_size

        # Muoviamo l'oggetto e verifichiamo le collisioni
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
            self.rect.x -= dx  # Annulliamo il movimento se c'è una collisione

        self.rect.y += dy
        if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
            self.rect.y -= dy  # Annulliamo il movimento se c'è una collisione

        # Applica la gravità automaticamente
        self.apply_gravity(obstacles)

# def draw_piece(piece):
#     color = random.choice(colors)
#     for i in range(len(piece.shape)):
#         for j in range(len(piece.shape[i])):
#             if piece.shape[i][j]:
#                 pygame.draw.rect(screen, color, (WIDTH // 2 + j * CELL_SIZE, 0 + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# def falling_piece(piece):
#     global last_move_time
#     current_time = pygame.time.get_ticks()
#     if current_time - last_move_time >= 1000:
#         piece.move(0, 1)
#         last_move_time = current_time

# def piece_down():
#     return piece.y + len(piece.shape) == HEIGHT // GRID_SIZE

all_pieces = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
last_move_time = pygame.time.get_ticks()
piece = Piece(random.choice(list(TETROMINOS.keys())), WIDTH // 2, 0, 30, random.choice(colors))
all_pieces.add(piece)
# draw_piece(piece)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            piece.y = HEIGHT


    # Things to do
    # if not pygame.sprite.spritecollide(piece, all_pieces, False) and not piece.y == HEIGHT:
    #     piece = Piece(random.choice(list(TETROMINOS.values())), WIDTH // 2, 0)
    #     all_pieces.add(piece)
    #     draw_piece(piece)
    # falling_piece(piece)

    piece.update(all_pieces)
    screen.fill(BLACK)
    all_pieces.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# class Tetris:
#     def __init__(self):
#         self.grid = [[0] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)]
#         self.current_piece = random.choice(TETROMINOS)
#         self.current_x = WIDTH // 2
#         self.current_y = 0

# # Creazione dello sprite
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()  # Inizializza lo sprite
#         self.image = pygame.Surface((50, 50))  # Crea un quadrato 50x50
#         self.image.fill(RED)  # Colora di rosso
#         self.rect = self.image.get_rect()  # Crea la hitbox
#         self.rect.x, self.rect.y = 100, 100  # Posizione iniziale

#     def update(self):
#         """Aggiorna la posizione del giocatore con i tasti"""
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= 5
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += 5
#         if keys[pygame.K_UP]:
#             self.rect.y -= 5
#         if keys[pygame.K_DOWN]:
#             self.rect.y += 5

# # Crea il giocatore
# player = Player()

# # Gruppo di sprite
# all_sprites = pygame.sprite.Group()
# all_sprites.add(player)

# # Game loop
# running = True
# clock = pygame.time.Clock()

# while running:
#     screen.fill(BLACK)

#     # Controllo eventi
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Aggiorna e disegna gli sprite
#     all_sprites.update()
#     all_sprites.draw(screen)

#     pygame.display.flip()
#     clock.tick(60)  # 60 FPS

# pygame.quit()
