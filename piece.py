import pygame
import random
from dimensions import *

# Pezzi di Tetris
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

    def on_ground(self, obstacles):
        """Porta il pezzo a terra"""
        self.rect.y = GRID_SIZE * (ROWS - len(self.matrix))  # Calcola la posizione in base alla griglia
        

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