import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)