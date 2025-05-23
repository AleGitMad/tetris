import pygame
from block import Block
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
bottom = [[1, 1, 1, 1, 1, 1, 1, 1]]

class Piece(pygame.sprite.Sprite):
    def __init__(self, shape, x, y, block_size=30, color=(255, 255, 255)):
        super().__init__()
        self.shape = shape
        self.block_size = block_size
        self.color = color
        # Se shape è una stringa, prendi la matrice da TETROMINOS
        if isinstance(shape, str) and shape in TETROMINOS:
            self.matrix = TETROMINOS[shape]
        else:
            # Altrimenti usa la matrice passata (bottom)
            self.matrix = shape
        
        self.collision = False  # Flag per la collisione

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
        # self.mask = expand_mask(self.mask)  # Espandi la maschera

        self.move_timers = {
            pygame.K_LEFT: {'pressed': False, 'start_time': 0, 'last_move': 0},
            pygame.K_RIGHT: {'pressed': False, 'start_time': 0, 'last_move': 0},
            pygame.K_DOWN: {'pressed': False, 'start_time': 0, 'last_move': 0},
            pygame.K_UP: {'pressed': False}
        }
        # Delay per il movimento
        self.move_delay_initial = 300  # ms
        self.move_delay_repeat = 100   # ms

    def rotate(self, obstacles):
        """Ruota la matrice del Tetromino di 90°"""
        if not pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
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

    def handle_key_events(self, event):
        """Gestisce gli eventi di pressione dei tasti per il movimento e la rotazione"""
        if event.type == pygame.KEYDOWN:
            if event.key in self.move_timers:
                self.move_timers[event.key]['pressed'] = True
                if event.key != pygame.K_UP:
                    self.move_timers[event.key]['start_time'] = pygame.time.get_ticks()
                    self.move_timers[event.key]['last_move'] = 0  # Forza lo spostamento iniziale
        elif event.type == pygame.KEYUP:
            if event.key in self.move_timers:
                self.move_timers[event.key]['pressed'] = False
        elif event.type == pygame.K_SPACE:
            self.on_ground()

    def apply_gravity(self):
        """Fa cadere il pezzo ogni tot millisecondi"""
        now = pygame.time.get_ticks()
        if now - self.gravity_timer > 500:  # Tempo in ms (500 ms = 0.5 sec)
            self.gravity_timer = now
            self.rect.y += self.block_size

    def get_highest_point(self):
        """Restituisce la coordinata Y assoluta del punto più alto del Piece"""
        for row_idx, row in enumerate(self.matrix):
            if any(cell == 1 for cell in row):
                return self.rect.y + row_idx * self.block_size
        return self.rect.y + len(self.matrix) * self.block_size  # Se vuoto, restituisce il fondo

    def on_ground(self, obstacles):
        """Simula la discesa istantanea del pezzo fino al primo ostacolo, 
        allineandolo esattamente sopra senza sovrapposizioni."""
        while True:
            # sposto di un blocco verso il basso
            self.rect.y += self.block_size
            # controllo se ora colpisco un ostacolo
            if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
                # torno indietro di un blocco
                self.rect.y -= self.block_size
                # segnalo collisione
                self.collision = True
                break

    
    def explode_into_blocks(self):
        """Suddivide il pezzo nei singoli blocchi e li restituisce come lista"""
        blocks = pygame.sprite.Group()
        for row_idx, row in enumerate(self.matrix):
            for col_idx, val in enumerate(row):
                if val == 1:
                    x = self.rect.x + col_idx * self.block_size
                    y = self.rect.y + row_idx * self.block_size
                    block = Block(x, y, self.block_size, self.color)
                    blocks.add(block)
        return blocks
        
    def update(self, obstacles, game_map):
        current_time = pygame.time.get_ticks()
        dx, dy = 0, 0

        # Movimento controllato (sinistra, destra, giù)
        for key, direction in [(pygame.K_LEFT, (-self.block_size, 0)),
                               (pygame.K_RIGHT, (self.block_size, 0)),
                               (pygame.K_DOWN, (0, self.block_size))]:
            state = self.move_timers[key]
            if state['pressed']:
                elapsed = current_time - state['start_time']
                interval = self.move_delay_repeat if elapsed > self.move_delay_initial else self.move_delay_initial
                if current_time - state['last_move'] >= interval:
                    if key == pygame.K_LEFT and self.rect.x > 0:
                        dx += direction[0]
                    elif key == pygame.K_RIGHT and self.rect.x + self.rect.width < WIDTH_G:
                        dx += direction[0]
                    elif key == pygame.K_DOWN and self.rect.y + self.rect.height < HEIGHT:
                        dy += direction[1]
                    state['last_move'] = current_time

        # Rotazione: solo al primo evento KEYDOWN
        if self.move_timers[pygame.K_UP]['pressed']:
            self.rotate(obstacles)
            self.move_timers[pygame.K_UP]['pressed'] = False  # Impedisci ripetizione fino al rilascio

        # Muoviamo l'oggetto e verifichiamo le collisioni
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
            self.rect.x -= dx  # Annulliamo il movimento se c'è una collisione
        self.rect.y += dy
        # Verifica collisione al suolo
        if self.rect.y + self.rect.height > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.collision = True
        if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
            self.rect.y -= dy  # Annulliamo il movimento se c'è una collisione

        # Applica la gravità automaticamente
        if not self.collision:
            self.apply_gravity()

        # Dopo gravità, verifica collisione in basso
        if pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask):
            self.rect.y -= self.block_size  # Torna indietro
            self.collision = True
        
        if self.collision:
            blocks = self.explode_into_blocks()
            for block in blocks:
                game_map.add_block(block)


def expand_mask(mask):
    """Espande una maschera Pygame aggiungendo un bordo di `expansion` pixel attorno"""
    width, height = mask.get_size()

    # Creiamo una nuova maschera più grande
    new_mask = pygame.mask.Mask((width + 2*GRID_SIZE, height + 2*GRID_SIZE))

    # Copiamo la maschera originale nella nuova, spostandola al centro
    for x in range(width):
        for y in range(height):
            if mask.get_at((x, y)):  # Se il pixel è attivo nella maschera originale
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        new_x = x + 1 + dx
                        new_y = y + 1 + dy
                        new_mask.set_at((new_x, new_y), 1)
    return new_mask