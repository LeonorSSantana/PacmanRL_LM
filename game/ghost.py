# game/ghost.py
import pygame


class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/ghost_sprites.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, maze):
        # TODO: Implement Ghost movement logic
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)
