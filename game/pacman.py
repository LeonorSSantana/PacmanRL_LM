# game/pacman.py
import pygame


class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/pacman_sprites.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, maze):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5
        self.rect.topleft = (self.x, self.y)
        # TODO: Add collision detection with maze walls

    def render(self, screen):
        screen.blit(self.image, self.rect)
