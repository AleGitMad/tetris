import pygame

class Map:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # questa va tolta
    def add_piece(self, piece):
        """Aggiorna la griglia con la posizione corrente del pezzo"""
        start_row = piece.rect.y // self.cell_size
        start_col = piece.rect.x // self.cell_size

        for y, row in enumerate(piece.matrix):
            for x, val in enumerate(row):
                if val:
                    grid_y = start_row + y
                    grid_x = start_col + x
                    if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
                        self.grid[grid_y][grid_x] = 1

    def add_block(self, block):
        """Aggiorna la griglia con la posizione corrente del blocco"""
        grid_x = block.rect.x // self.cell_size
        grid_y = block.rect.y // self.cell_size
        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            self.grid[grid_y][grid_x] = 1  # o potresti memorizzare il `block` stesso se ti serve accesso diretto


    def clear_full_rows(self):
        """Controlla e rimuove righe complete, ritorna gli indici delle righe rimosse"""
        full_rows = [i for i, row in enumerate(self.grid) if all(cell == 1 for cell in row)]
        for i in full_rows:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(self.cols)])  # Aggiungi riga vuota in cima
        return full_rows

    def draw(self, surface, color=(100, 100, 100)):
        """Disegna la griglia di stato (debug o effetti visivi)"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]:
                    pygame.draw.rect(surface, color,
                                     (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
