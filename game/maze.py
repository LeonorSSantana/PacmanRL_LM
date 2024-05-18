# game/maze.py
import pygame


class Maze:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (800, 600))

    def render(self, screen):
        screen.blit(self.image, (0, 0))
